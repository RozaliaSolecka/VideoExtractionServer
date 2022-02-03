import logging
import os
import time
from typing import List

import ray
from ray.util import ActorPool
from ray.util.queue import Queue

import config
from neural_network.detection.detection_filterer import DetectionFilterer
from neural_network.detection.i_detection_filterer import IDetectionFilterer
from model.classification_result import ClassificationResult
from model.detected_output import DetectedOutput
from model.video_frame import VideoFrame
from remotes.classification_remote import ClassifierRemote
from remotes.model.object_to_classify import ObjectToClassify
from remotes.video_remote import VideoRemote
from static_functions import save_detected_photos, save_original_frame
from .base_source_service import BaseSourceService
from .video.detection_service import DetectionService
from .video.model.detection_state import DetectionState
from .video.results_service import ResultsService


class VideoService(BaseSourceService):
    """
    Service to process the video stream from the provided file
    """
    def __init__(self):
        super().__init__()

        # init logger
        try:
            os.remove('../times.log')
        except OSError:
            pass
        handler = logging.FileHandler('../times.log', mode='a+')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [VIDEO_SERVICE] %(message)s')
        handler.setFormatter(formatter)
        self.__logger = logging.getLogger('times')
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(handler)
        self.__logger.propagate = False

        # init ray library used for multiprocessing
        ray.init()

        # init queue for incoming frames
        self.__video_queue = Queue()

        # init internal dependencies
        self.__detection_filterer: IDetectionFilterer = DetectionFilterer()
        self.__results_service = ResultsService(config.cfg.getint(config.VIDEO, 'max_number_of_classifications'))
        self.__detection_state = DetectionState(self.__results_service,
                                                config.cfg.getint(config.VIDEO, 'classifier_interval_break'),
                                                config.cfg.getint(config.VIDEO, 'empty_frames_limit'))
        self.__detection_service = DetectionService(self.__detection_filterer, self.__logger,
                                                    self._detectorController, self._detectionOutputFormatter)

        # private fields
        self.__frame_index = 0

        # init classification
        self.__classifier_queue = Queue()
        classifier_remotes = [
            ClassifierRemote.remote(config.cfg.get(config.CLASSIFIER, 'model_path'),
                                    self.__classifier_queue,
                                    config.cfg.getboolean(config.VIDEO, 'save_debug_frames'))
            for _ in range(2)
        ]
        self.__classifier_pool = ActorPool(classifier_remotes)
        # wait for the classifier to be loaded, detector is loaded with init of this service
        for remote in classifier_remotes:
            ray.get(remote.wait.remote(), timeout=180)

    def service(self) -> None:
        last_frame_time = 0

        # start reading the video in the another process
        video_remote = VideoRemote.remote(config.cfg.getint(config.VIDEO, 'fps'))
        if config.cfg.getboolean(config.VIDEO, 'benchmark_mock'):
            video_remote.benchmark_mock.remote(self.__video_queue)
        else:
            video_remote.video.remote(self.__video_queue, config.cfg.get(config.VIDEO, 'path'))

        while True:
            # perform detection if frame is ready and send it for classification if needed
            if not self.__video_queue.empty():
                last_frame_time = time.time()

                # get video frame
                start_time = time.time()
                video_frame: VideoFrame = self.__video_queue.get()
                exec_time = time.time() - start_time
                time_msg = "getting frame from queue time:  %8.2f ms" % (1000 * exec_time)
                self.__logger.info(time_msg)
                self.__frame_index = video_frame.index

                self.__logger.info(f"FRAME {self.__frame_index} PASSED TO DETECTOR")
                video_queue_length = self.__video_queue.qsize()
                self.__logger.info(f"VIDEO QUEUE LEN: {video_queue_length}")
                if video_queue_length > 3:
                    self.__logger.error(
                        "Video queue is bigger than 3, so detection is too slow for this number of frames per second!"
                        " Try to reduce number of frames per second!")

                detected_output, video_frame.index = self.__detection_service\
                    .detect(video_frame.frame, video_frame.index)

                if config.cfg.getboolean(config.VIDEO, 'save_debug_frames'):
                    save_original_frame(video_frame.frame, video_frame.index)
                    crop_img_list = self._imageCropper.format(video_frame.frame, detected_output)
                    save_detected_photos(crop_img_list, video_frame.index)

                self.__processDetectionResult(detected_output, video_frame)

            # handle classification result
            if not self.__classifier_queue.empty():
                self.__classifier_pool.get_next()
                classification_result: ClassificationResult = self.__classifier_queue.get()
                self.__logger.info(f"CLASSIFICATION OF OBJECT {classification_result.obj_index} ON FRAME "
                             f"{classification_result.frame_index} FINISHED")
                self.__results_service \
                    .addClassificationResult(classification_result.obj_index, classification_result.class_name)

                if self.__results_service.isFinished(classification_result.obj_index):
                    self.__results_service.finishObject(classification_result.obj_index)

                if self.__frame_index - classification_result.frame_index > 10:
                    self.__logger.error(
                        "Classification result is more than 10 frames late, so classification is too slow for this "
                        "number of frames per second! Try to reduce number of frames which are classified!")

            # handle when program is finished
            else:
                if last_frame_time != 0 and time.time() - last_frame_time > 5:
                    self.__logger.info("End of video")
                    exit(0)

    def __processDetectionResult(self, detection_info: List[DetectedOutput], video_frame: VideoFrame):
        if len(detection_info) > 1:
            self.__logger.warning(f"More than one object detected on frame {video_frame.index}. Object that entered "
                            f"the detection zone as the last one is being processed.")
            detection_info = [detection_info[0]]

        if len(detection_info) == 1:
            if self.__detection_state.isNewObject(detection_info[0]):
                self.__detection_state.handleNewObject()

            if self.__results_service.shouldSendToClassify(self.__detection_state.getObjectId()) and \
                    self.__detection_state.isReadyForClassification():
                crop_img_list = self._imageCropper.format(video_frame.frame, detection_info)
                self.__logger.info(f"FRAME {video_frame.index} PASSED TO CLASSIFICATION")
                self.__classifier_pool.submit(
                    lambda a, v: a.classify.remote(v),
                    ObjectToClassify(crop_img_list, video_frame.index, self.__detection_state.getObjectId()))
                self.__results_service.expectClassification(self.__detection_state.getObjectId())
                self.__detection_state.handleClassifiedFrame()

            self.__results_service.updateLastPosition(self.__detection_state.getObjectId(),
                                                      detection_info[0], video_frame.timestamp)

        self.__detection_state.handleAnyFrame(len(detection_info) == 1)
