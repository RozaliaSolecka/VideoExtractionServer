import tensorflow as tf
from tensorflow.python.saved_model import tag_constants

from .i_neural_network_loader import INeuralNetworkLoader


class TFNeuralNetworkLoader(INeuralNetworkLoader):
    def load_model(self, load_path) -> None:
        return tf.saved_model.load(load_path, tags=[tag_constants.SERVING])
