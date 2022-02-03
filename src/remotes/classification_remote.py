import logging
import string
import time

import ray
import tensorflow as tf
from ray.util.queue import Queue

from model.classification_result import ClassificationResult
from neural_network.classification.keras.keras_classifier_controller import KerasNeuralNetworkClassifier
from remotes.model.object_to_classify import ObjectToClassify
from static_functions import save_classified_photos


@ray.remote(num_cpus=1, num_gpus=0.5)
class ClassifierRemote:
    """
    Async classification of object which were detected earlier.
    """
    def __init__(self, path: string, queue: Queue, save_debug_frames: bool):
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

        """
        :param path: path to the classifier model
        """
        self.__classifier = KerasNeuralNetworkClassifier(path)
        self.__queue = queue
        self.__save_debug_frames = save_debug_frames
        logging.basicConfig(level=logging.INFO, filename='../times.log',
                            filemode='a+', format='[CLASSIFIER][%(thread)d] %(message)s') 

    def wait(self):
        """
        Waits for the neural network to be fully loaded
        """
        pass

    def classify(self, object_to_classify: ObjectToClassify):
        """
        Classifies list of images with detected objects and saves images to the disk.
        :param object_to_classify: describes the object to classify
        :return:
        """
        start_time = time.time()
        classification_results = self.__classifier.predict(object_to_classify.crop_img_list)
        exec_time = time.time() - start_time
        time_msg = f"FRAME {object_to_classify.frame_index}: classification time of " \
                   f"{len(object_to_classify.crop_img_list)} images : {(1000 * exec_time):.2f} ms"
        logging.info(time_msg)

        self.__queue.put(ClassificationResult(object_to_classify.object_id,
                                              classification_results.classification_classes[0],
                                              object_to_classify.frame_index))

        if self.__save_debug_frames:
            save_classified_photos(object_to_classify.crop_img_list, classification_results,
                                   object_to_classify.frame_index)
