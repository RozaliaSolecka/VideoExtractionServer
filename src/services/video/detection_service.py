import time
from logging import Logger
from typing import List

from ray.util.queue import Queue

from neural_network.detection.i_detection_filterer import IDetectionFilterer
from neural_network.detection.output_formatters.i_detection_output_formatter import IDetectionOutputFormatter
from model.detected_output import DetectedOutput
from neural_network.detection.base_detector_controller import BaseDetectorController


class DetectionService:
    """
    Service which can perform detection for the single frame
    """
    def __init__(self,
                 detection_filterer: IDetectionFilterer,
                 logger: Logger,
                 detection_controller: BaseDetectorController,
                 detection_formatter: IDetectionOutputFormatter
                 ) -> None:
        """
        :param detection_filterer: filterer for detection results
        :param logger: logger
        :param detection_controller: controller which allows to perform detection
        :param detection_formatter: service to format plain detection results
        """
        self.__detection_filterer = detection_filterer
        self.__logger = logger
        self.__detectorController = detection_controller
        self.__detectionOutputFormatter = detection_formatter

    def detect(self, frame, frame_index) -> (List[DetectedOutput], int):
        start_time = time.time()

        prediction, original_w, original_h = self.__detectorController.predict(frame)
        detection_info = self.__detectionOutputFormatter.format(prediction, original_w, original_h)
        detection_info = sorted(detection_info, key=lambda x: x.relative_center_x())

        if len(detection_info) > 0:
            detection_info = self.__detection_filterer.filter(detection_info)

        exec_time = time.time() - start_time
        time_msg = "detection + formatting time:  %8.2f ms" % (1000 * exec_time)
        self.__logger.info(time_msg)

        return detection_info, frame_index
