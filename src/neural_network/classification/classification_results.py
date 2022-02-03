from typing import List


class ClassificationResults:
    def __init__(self, classification_classes: List[str], classification_scores: List[float]):
        """
        Describes the result of classification prediction
        :param classification_classes: list of predicted classes
        :param classification_scores: confidence of predicted scores
        """
        self.classification_classes = classification_classes
        self.classification_scores = classification_scores

    @staticmethod
    def from_dict(classification_results_dict):
        return ClassificationResults(classification_results_dict['classification_classes'],
                                     classification_results_dict['classification_scores'])

    @staticmethod
    def empty():
        return ClassificationResults([], [])

    def get_as_dict(self):
        return {'classification_classes', self.classification_classes,
                'classification_scores', self.classification_scores}
