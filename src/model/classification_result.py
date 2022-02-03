class ClassificationResult:
    """
    Object describing classification result
    """
    def __init__(self,
                 obj_index: int,
                 class_name: str,
                 frame_index: int) -> None:
        """
        :param obj_index: global index of object
        :param class_name: class name classified for object
        :param frame_index: id of the frame where the object was present
        """
        super().__init__()
        self.obj_index = obj_index
        self.class_name = class_name
        self.frame_index = frame_index
