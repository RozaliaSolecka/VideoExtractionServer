import configparser

cfg = configparser.ConfigParser()

APP = 'APP'
CLASSIFIER = 'CLASSIFIER'
DETECTOR = 'DETECTOR'
PHOTO = 'PHOTO'
VIDEO = 'VIDEO'


class Config:
    def __init__(self, path: str) -> None:
        super().__init__()
        cfg.read(path)
