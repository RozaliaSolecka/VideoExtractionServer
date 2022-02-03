from abc import ABCMeta, abstractmethod
from typing import List

from model.detected_output import DetectedOutput


class IDetectionFilterer:
    __metaclass__ = ABCMeta

    @abstractmethod
    def filter(self, detected_output: List[DetectedOutput]) -> List[DetectedOutput]:
        """
        Removes unwanted detections. Those include:
        - doubled detections for the single object (sorted out from centre position of detections)
        - detections on the edge of the frame because they potentially contain only part of the object
        :param detected_output: list of detections from the detector
        :return: detections with removed unwanted detections
        """
        raise NotImplementedError
