import logging
import string
import time
from typing import List

import numpy as np
from numpy import ndarray
from tensorflow import keras

from neural_network.classification.classification_results import ClassificationResults
from neural_network.classification.keras.resize_transformation import ResizeTransformation
from neural_network.classification.lego_classifier import LegoClassifier


class KerasNeuralNetworkClassifier(LegoClassifier):
    def __init__(self, model_path: string):
        """
        Classifier based on keras format of the saved model
        :param model_path: file path to the model weights
        """
        super().__init__()
        self.model_path = model_path
        self.model = keras.models.load_model(self.model_path)
        self.size = (224, 224)
        # first prediction is longer so first run is dry
        self.model(np.vstack(np.ones((1, 1, 224, 224, 3), dtype=np.float32)))

    def predict(self, images: List[ndarray]) -> ClassificationResults:
        if len(images) == 0:
            return ClassificationResults.empty()

        images_array = []
        start_time = time.time()

        for img in images:
            transformed = ResizeTransformation.transform(img, self.size)
            img_array = np.expand_dims(transformed, axis=0)
            images_array.append(img_array)
        processing_elapsed_time_ms = 1000 * (time.time() - start_time)

        predictions = self.model(np.vstack(images_array))

        predicting_elapsed_time_ms = 1000 * (time.time() - start_time) - processing_elapsed_time_ms

        logging.info(f"[KerasClassifier] Preparing images took {processing_elapsed_time_ms} ms, "
                     f"when predicting took {predicting_elapsed_time_ms} ms.")

        indices = [int(np.argmax(values)) for values in predictions]
        classes = [self.class_names[index] for index in indices]
        scores = [float(prediction[index]) for index, prediction in zip(indices, predictions)]

        return ClassificationResults(classes, scores)
