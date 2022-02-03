import logging
import typing
from datetime import datetime

from model.detected_output import DetectedOutput
from services.video.model.object_results import ObjectResults, PositionWithTime, ResultState
from static_functions import toJSON


class ResultsService:
    def __init__(self, max_number_of_classifications) -> None:
        """
        :param max_number_of_classifications: configurable max number of classification per single object before
            it is marked as classified sufficiently
        """
        self.__dictionary: typing.Dict[int, ObjectResults] = dict()
        self.__max_number_of_classifications = max_number_of_classifications

        # defines how many historical values are stored in the collection
        self.__history_threshold = 5

        handler = logging.FileHandler('../results.log', mode='w')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        self.logger = logging.getLogger('results')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def __createEntry(self, key: int):
        self.__dictionary[key] = ObjectResults()

    def addClassificationResult(self, key: int, val: str) -> None:
        """
        Appends classification result.
        :param key: id of the object
        :param val: classified class for the object
        """
        if key not in self.__dictionary:
            self.__createEntry(key)
        self.__dictionary[key].addClassifiedClass(val)

    def expectClassification(self, key: int) -> None:
        """
        Adds next expectation for classification for the object.
        :param key: Id of the object which should have one more classification.
        """
        if key not in self.__dictionary:
            self.__createEntry(key)
        self.__dictionary[key].addExpectedClassification()

    def objectLeftDetectionZone(self, key: int) -> None:
        """
        Handle event when object left detection zone or has its all classification submitted
        :param key: Global object index
        """
        if key not in self.__dictionary:
            return

        item = self.__dictionary[key]
        item.leftDetectionZone()

        if self.isFinished(key):
            self.finishObject(key)

    def shouldSendToClassify(self, key: int) -> bool:
        """
        Checks whether the classification should be performed for the item with given global key
        :param key: Global object index
        :return: True if next frame for the object should be classified.
        """
        if key not in self.__dictionary:
            return True

        item = self.__dictionary[key]

        if item.has_left_detection_zone is True:
            return False

        # limit for classification of object
        if item.expected_number_of_classifications == self.__max_number_of_classifications:
            item.has_left_detection_zone = True
            return False

        return True

    def isFinished(self, key: int) -> bool:
        """
        Check whether classification process for the object has finished
        :param key: global object index
        :return: true if object is ready to create final result to send
        """
        item = self.__dictionary[key]
        return (not self.shouldSendToClassify(key)) and item.isAllClassified() and \
            item.state is not ResultState.FINISHED

    def finishObject(self, key: int) -> None:
        """
        Create final result of the object classification
        :param key: global object index
        """
        item = self.__dictionary[key]
        result = item.createResult()
        position = toJSON(item.lastPosition)
        self.logger.info(f"Object {key} result class: {result[0]}. Position: {position}")
        self.logger.debug(result)

        # clean object in history if exists to not fill the collection infinitely
        if key - 5 in self.__dictionary:
            self.__dictionary.pop(key - 5)

    def updateLastPosition(self, key: int, detection: DetectedOutput, frame_timestamp: datetime):
        """
        Saves last detected position of the object
        :param key: id of the object
        :param detection: result of the detection for this object
        :param frame_timestamp: timestamp where the frame was received
        :return:
        """
        if key not in self.__dictionary:
            self.__createEntry(key)
        item = self.__dictionary[key]

        item.lastPosition = PositionWithTime(
            detection.relative_center_x(), detection.relative_center_y(),
            frame_timestamp)


