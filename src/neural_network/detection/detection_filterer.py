from typing import List

from neural_network.detection.i_detection_filterer import IDetectionFilterer
from model.detected_output import DetectedOutput


class DetectionFilterer(IDetectionFilterer):
    def __init__(self):
        self.__duplicateThreshold = 0.01
        self.__edgeThreshold = 0.05

    def filter(self, detected_output: List[DetectedOutput]) -> List[DetectedOutput]:
        result = self.__filterDuplicated(detected_output)
        return self.__filterNearEdge(result)

    def __filterDuplicated(self, detected_output: List[DetectedOutput]) -> List[DetectedOutput]:
        previous = detected_output[0]
        results = [previous]
        for result in detected_output[1:]:
            if abs(result.relative_center_x() - previous.relative_center_x()) > self.__duplicateThreshold:
                results.append(result)
            else:
                # leave the detection with bigger bounding box which gives bigger chance that detection is not partial
                if previous.width() < result.width():
                    results.pop()
                    results.append(result)
            previous = result
        return results

    def __filterNearEdge(self, detected_output: List[DetectedOutput]) -> List[DetectedOutput]:
        results = []
        for result in detected_output:
            if result.relative_x_min() > self.__edgeThreshold and 1.0 - result.relative_x_max() > self.__edgeThreshold and \
                result.relative_y_min() > self.__edgeThreshold and 1.0 - result.relative_y_max() > self.__edgeThreshold:
                results.append(result)
        return results
