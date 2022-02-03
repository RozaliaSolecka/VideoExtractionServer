import string
from abc import ABCMeta, abstractmethod
from typing import Any


class INeuralNetworkLoader:
    __metaclass__ = ABCMeta

    @abstractmethod
    def load_model(self, model_path: string) -> Any:
        """
        Load the neural network model for specific libraries
        :param model_path: file path to the model
        :return: loaded model of neural network
        """
        raise NotImplementedError
