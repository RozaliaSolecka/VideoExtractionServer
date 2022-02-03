from pathlib import Path
from typing import List

from numpy import ndarray

from neural_network.classification.classification_results import ClassificationResults


class LegoClassifier:
    """
    Class which can perform prediction of lego model.
    """
    def __init__(self):
        self.class_names: List[str] = self.read_classes_from_file()

    def predict(self, images: [ndarray]) -> ClassificationResults:
        """
        Perform prediction on the list of images
        :param images: list of the images
        :return: List of classification results
        """
        pass

    @staticmethod
    def read_classes_from_file(classes_file="./data/classes.txt") -> List[str]:
        with open(Path(classes_file)) as file:
            return [class_str.strip() for class_str in file]
