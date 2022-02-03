import cv2
from numpy import ndarray

from neural_network.classification.keras.transformation import Transformation


class ResizeTransformation(Transformation):

    @staticmethod
    def transform(img: ndarray, desired_size: (int, int) = (299, 299)) -> ndarray:
        """
        Resize transformation
        :param img: source image
        :param desired_size: resolution after the transformation
        :return: resized image
        """
        transformed = cv2.resize(img, desired_size, interpolation=cv2.INTER_AREA)
        return transformed

