from pathlib import Path

import cv2

import config
from neural_network.classification.keras.keras_classifier_controller import KerasNeuralNetworkClassifier
from neural_network.classification.lego_classifier import LegoClassifier
from static_functions import save_classified_photos
from .base_source_service import BaseSourceService


class PhotoService(BaseSourceService):
    """
    Service to process sequentially the images stored in a provided folder
    """
    def __init__(self):
        super().__init__()
        self._classifier: LegoClassifier = \
            KerasNeuralNetworkClassifier(config.cfg.get(config.CLASSIFIER, 'model_path'))

    def service(self) -> None:
        files = Path(config.cfg.get(config.PHOTO, 'path')).glob('*')

        files = filter(lambda x: x.is_file and x.name.endswith('.jpg'), files)

        for file in files:
            image = cv2.imread(str(file))
            prediction, original_w, original_h = self._detectorController.predict(image)
            detection_info = self._detectionOutputFormatter.format(prediction, original_w, original_h)
            detection_info = sorted(detection_info, key=lambda x: x.relative_center_y(), reverse=True)

            crop_img_list = self._imageCropper.format(image, detection_info)

            classification_results = self._classifier.predict(crop_img_list)

            save_classified_photos(crop_img_list, classification_results, file.name.ljust(10, '_')[:10])


