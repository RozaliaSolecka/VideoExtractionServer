from typing import List

from numpy import ndarray


class ObjectToClassify:
    """
    Describes the object which requires the classification
    """
    def __init__(self, crop_img_list: List[ndarray], frame_index: int, object_id: int) -> None:
        """
        :param crop_img_list: list of the cropped image containing detected images
        :param frame_index: global index of the frame
        :param object_id: global index of the detected object
        """
        self.crop_img_list = crop_img_list
        self.frame_index = frame_index
        self.object_id = object_id
