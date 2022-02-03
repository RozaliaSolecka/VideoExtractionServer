from abc import ABCMeta, abstractmethod

import config
from neural_network.detection.output_formatters.i_detection_output_formatter import IDetectionOutputFormatter
from neural_network.detection.output_formatters.yolov4_tiny_detection_output_formatter import YoloV4TinyDetectionOutputFormatter
from neural_network.detection.output_formatters.yolov5_detection_output_formatter import YoloV5DetectionOutputFormatter
from image.i_image_cropper import IImageCropper
from image.image_cropper import ImageCropper
from neural_network.detection.base_detector_controller import BaseDetectorController
from neural_network.detection.yolov4_detector_controller import YoloV4TinyDetectorController
from neural_network.detection.yolov5_detector_controller import YoloV5DetectorController


class BaseSourceService:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._counter = 0
        self._imageCropper: IImageCropper = ImageCropper()
        if config.cfg.getboolean(config.DETECTOR, 'use_yolo_v5'):
            self._detectorController: BaseDetectorController = \
                YoloV5DetectorController(config.cfg.get(config.DETECTOR, 'model_path'))
            self._detectionOutputFormatter: IDetectionOutputFormatter = YoloV5DetectionOutputFormatter()
        else:
            self._detectorController: BaseDetectorController = \
                YoloV4TinyDetectorController(config.cfg.get(config.DETECTOR, 'model_path'))
            self._detectionOutputFormatter: IDetectionOutputFormatter = YoloV4TinyDetectionOutputFormatter()

    @abstractmethod
    def service(self) -> None: raise NotImplementedError
