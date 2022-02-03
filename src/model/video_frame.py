from datetime import datetime

from numpy import ndarray


class VideoFrame:
    def __init__(self, frame: ndarray, index: int, timestamp: datetime):
        """
        Object describing single video frame
        :param frame: content of the frame
        :param index: frame identifier
        :param timestamp: timestamp when the frame was recorded
        """
        self.frame = frame
        self.index = index
        self.timestamp = timestamp
