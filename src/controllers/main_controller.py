import config
from src.services.base_source_service import BaseSourceService
from src.services.photo_service import PhotoService
from src.services.video_service import VideoService


class MainController:
    """
    Chooses correct type of the whole processing
    """
    def __init__(self):
        if config.cfg.getboolean(config.APP, 'picture'):
            self.__sourceService: BaseSourceService = PhotoService()
        else:
            self.__sourceService: BaseSourceService = VideoService()

    def run(self) -> None:
        self.__sourceService.service()
