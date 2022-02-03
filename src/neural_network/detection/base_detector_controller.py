from abc import ABCMeta, abstractmethod
from typing import Any, Tuple

import cv2
import numpy as np


class BaseDetectorController:
    __metaclass__ = ABCMeta

    @abstractmethod
    def predict(self, image) -> Tuple[Any, int, int]:
        """
        Load and prepare image for performing detection
        :param image: source image
        :return: Tuple containing not formatted neural network result, its original width, and height
        """
        raise NotImplementedError

    def _load_image_pixels(self, image) -> Tuple[Any, int, int]:
        """
        Load and prepare image for performing detection
        :param image: source image
        :return: Tuple containing image, its original width, and height
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        image = cv2.resize(image, (416, 416))
        image = image / 255.
        image = image[np.newaxis, ...].astype(np.float32)
        return image, width, height
