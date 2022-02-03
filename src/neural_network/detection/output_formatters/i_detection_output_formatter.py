from abc import ABCMeta, abstractmethod
from typing import List

from model.detected_output import DetectedOutput


class IDetectionOutputFormatter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, base_output, image_w, image_h) -> List[DetectedOutput]:
        """
        Formats the output form the neural network
        :param base_output: raw result of the run on neural network
        :param image_w: original width of the image
        :param image_h: original height of the image
        :return: Detection result in the common format
        """
        raise NotImplementedError
