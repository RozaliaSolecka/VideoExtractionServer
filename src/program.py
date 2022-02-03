import argparse

from config import Config
from controllers.main_controller import MainController
from static_functions import *

parser = argparse.ArgumentParser(description='Simple loaded NN')
parser.add_argument('-c', '--config', type=str, help="specify the path to config different than default",
                    nargs='?', const=True, default='../config.ini')
args = parser.parse_args()


class Program(object):
    def __init__(self):
        prepare_frames_folder('../output')
        self.__mainController = MainController()

    def run(self):
        self.__mainController.run()


if __name__ == '__main__':
    Config(args.config)    # read config
    Program().run()
