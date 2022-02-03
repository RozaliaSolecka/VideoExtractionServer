import typing
from collections import Counter
from enum import Enum

from model.position_with_time import PositionWithTime


class ResultState(Enum):
    """
    Describes the status of the ObjectResults object
    """
    ACTIVE = 1
    WAITING = 2
    FINISHED = 3


class ObjectResults:
    """
    Describes multiple classification consecutive results of the single detected object
    """
    def __init__(self) -> None:
        # how many frames were send for classification
        self.expected_number_of_classifications: int = 0
        # list of the classified classes for the object
        self.__classification_list: typing.List[str] = []
        # indicates whether the object left the detection zone or have enough frames classified
        self.has_left_detection_zone: bool = False
        # current state of the object classification
        self.state: ResultState = ResultState.ACTIVE
        self.lastPosition: PositionWithTime = None

    def addClassifiedClass(self, class_name: str) -> None:
        """
        Add new classification for the object
        :param class_name: class name
        """
        self.__classification_list.append(class_name)

    def addExpectedClassification(self) -> None:
        """
        Adds one to expected classifications of the object. It means that one more frame was sent to classification
        for this object.
        """
        self.expected_number_of_classifications += 1

    def isAllClassified(self) -> bool:
        """
        Checks if all expected frames are classified if object left the detection state.
        :return: true if object can have final result ready to send.
        """
        return self.has_left_detection_zone and \
               len(self.__classification_list) == self.expected_number_of_classifications

    def leftDetectionZone(self) -> None:
        """
        Sets the correct state of the object after it has left detection zone
        """
        if self.state is ResultState.ACTIVE:
            self.state = ResultState.WAITING
        self.has_left_detection_zone = True

    def createResult(self) -> typing.Tuple[str, str]:
        """
        :return: Final result of the classification of the object
        """
        self.state = ResultState.FINISHED

        elements = self.__classification_list
        if len(elements) == 0:
            return 'undefined', '()'
        counter = Counter(elements)
        (dominantClass, occurrences) = counter.most_common(1)[0]

        if occurrences > len(elements) * 0.5:       # TODO: filter out results on single classifications (?)
            return dominantClass, str(counter)
        else:
            # classifications does not give unambiguous result
            return 'undefined', str(counter)
