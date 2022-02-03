from model.detected_output import DetectedOutput
from services.video.results_service import ResultsService


class DetectionState:
    """
    Object which is responsible for handling the state of the detection. It consists proper numbering of objects,
    keeping the intervals between classifications, checking whether new object came into detection zone.
    """
    def __init__(
            self, results_service: ResultsService,
            interval_length: int, empty_frames_limit):
        """
        :param results_service: results service
        :param interval_length: number of frames between possible consecutive classifications
        :param empty_frames_limit: number of frames without valid object before we decide to move for the next object
        """
        self.__interval_counter = 0
        self.__interval_length = interval_length
        self.__obj_counter = 0
        self.__empty_frames_limit = empty_frames_limit
        self.__empty_frames_counter = empty_frames_limit
        self.__previous_object_x_position = .0
        self.__previous_object_y_position = .0
        self.__results_service = results_service

        self.__y_position_delta_limit = 0.05

    def getObjectId(self):
        """
        :return: id of the current object
        """
        return self.__obj_counter

    def handleClassifiedFrame(self) -> None:
        """
        Handling of the frame after it was sent for classifications.
        Effectively it start the frame interval between sending the classification results.
        """
        self.__interval_counter = self.__interval_length + 1

    def handleNewObject(self) -> None:
        """
        Handling when the new object enters the detection zone.
        It starts the processing for the next object.
        """
        self.__results_service.objectLeftDetectionZone(self.__obj_counter)
        self.__obj_counter += 1

    def isNewObject(self, detection_output: DetectedOutput) -> bool:
        """
        Checks whether currently detected object seems to be the new one.
        :param detection_output: information about detected object
        :return: true if this is new object
        """
        x_position = detection_output.relative_center_x()
        previous_x = self.__previous_object_x_position
        self.__previous_object_x_position = x_position

        y_position = detection_output.relative_center_y()
        previous_y = self.__previous_object_y_position
        self.__previous_object_y_position = y_position

        # if position of new object is before the previous one, than it is a new object
        if x_position < previous_x:
            return True

        # if detected object is far from the previous one in y axis
        if abs(y_position - previous_y) > self.__y_position_delta_limit:
            return True

        # if there were too many empty frames without the detected object
        if self.__tooManyEmptyFrames():
            return True
        pass

    def isReadyForClassification(self) -> bool:
        """
        Informs whether application is ready to send next frame for classification based on defined interval.
        """
        return self.__interval_counter == 0

    def handleAnyFrame(self, is_frame_with_object: bool):
        """
        Handling for every frame
        :param is_frame_with_object: informs whether frame had object detected
        :return:
        """
        if is_frame_with_object:
            self.__empty_frames_counter = self.__empty_frames_limit
        elif self.__empty_frames_counter > 0:
            self.__empty_frames_counter -= 1

        if self.__interval_counter > 0:
            self.__interval_counter -= 1

    def __tooManyEmptyFrames(self) -> bool:
        """
        Checks if there were too many frames without detected object.
        :return: True means that next detected object should be handled like the new object.
        """
        return self.__empty_frames_counter == 0
