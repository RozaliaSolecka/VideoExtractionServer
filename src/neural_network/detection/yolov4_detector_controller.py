import string
from typing import Any, Tuple

import numpy as np
import tensorflow as tf

from .base_detector_controller import BaseDetectorController
from ..loader.i_neural_network_loader import INeuralNetworkLoader
from ..loader.tf_neural_network_loader import TFNeuralNetworkLoader

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


class YoloV4TinyDetectorController(BaseDetectorController):
    def __init__(self, path: string):
        self.__nnLoader: INeuralNetworkLoader = TFNeuralNetworkLoader()
        self.__model = self.__nnLoader.load_model(path)
        infer = self.__model.signatures['serving_default']
        # first prediction is longer so first run is dry
        batch_data = tf.constant(np.ones((1, 416, 416, 3), dtype=np.float32))
        infer(batch_data)

    def predict(self, image) -> Tuple[Any, int, int]:
        image, original_w, original_h = self._load_image_pixels(image)
        # make prediction
        infer = self.__model.signatures['serving_default']
        batch_data = tf.constant(image)
        prediction = infer(batch_data)
        return prediction, original_w, original_h
