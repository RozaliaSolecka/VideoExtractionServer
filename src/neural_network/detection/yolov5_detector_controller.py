import string
from typing import Any, Tuple

import cv2
import numpy as np
import torch

from neural_network.detection.base_detector_controller import BaseDetectorController


class YoloV5DetectorController(BaseDetectorController):
    def __init__(self, path: string) -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=path)
        if torch.cuda.is_available():
            self.model.cuda()
        image = np.ones((640, 640, 3), dtype=np.float32)
        self.model([image], size=image.shape[0])

    def predict(self, image) -> Tuple[Any, int, int]:
        image, original_w, original_h = self._load_image_pixels(image)
        prediction = self.model([image], size=image.shape[0])
        return prediction, original_w, original_h

    def _load_image_pixels(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width = image.shape[:2]
        image = cv2.resize(image, (640, 640))
        image = image.astype(np.float32)
        return image, width, height
