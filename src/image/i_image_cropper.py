from abc import ABCMeta, abstractmethod
from typing import List

from numpy import ndarray


class IImageCropper:
    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, images, bounding_boxes) -> List[ndarray]:
        """
        Crops the bounding boxes out of the images
        :param images: list of the images
        :param bounding_boxes: bounding boxes for those images
        :return:
        """
        raise NotImplementedError
