from abc import ABC, abstractmethod

from numpy import ndarray


class Transformation(ABC):
    @staticmethod
    @abstractmethod
    def transform(img: ndarray) -> ndarray:
        """
        Transformation on the image
        :param img: source img
        :return: image after transformation
        """
        ...
