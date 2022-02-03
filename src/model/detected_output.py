class DetectedOutput:
    def __init__(self, x_min: int, y_min: int, x_max: int, y_max: int, score: float, width: int, height: int):
        """
        Object describing the object detected on the frame
        :param x_min: smaller x coordinate of the bounding box around object
        :param y_min: bigger y coordinate of the bounding box around object
        :param x_max: bigger x coordinate of the bounding box around object
        :param y_max: smaller y coordinate of the bounding box around object
        :param score: confidence of the object presence
        :param width: width of the original image
        :param height: height of the original image
        """
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.score = score
        self.image_width = width
        self.image_height = height

    def relative_center_x(self) -> float:
        """
        :return: Relative center in x axis, where 0 is on the right side.
        """
        return 1 - ((self.x_max + self.x_min) / (2.0 * self.image_width))

    def relative_center_y(self) -> float:
        """
        :return: Relative center position in y axis
        """
        return 1 - ((self.y_max + self.y_min) / (2.0 * self.image_height))

    def relative_x_min(self) -> float:
        """
        :return: X min coordinate, as a float position in 0-1 range relative of the position in x axis
        """
        return 1.0 * self.x_min / self.image_width

    def relative_y_min(self) -> float:
        """
        :return: Y min coordinate, as a float position in 0-1 range relative of the position in y axis
        """
        return 1.0 * self.y_min / self.image_height

    def relative_x_max(self) -> float:
        """
        :return: X max coordinate, as a float position in 0-1 range relative of the position in x axis
        """
        return 1.0 * self.x_max / self.image_width

    def relative_y_max(self) -> float:
        """
        :return: Y max coordinate, as a float position in 0-1 range relative of the position in y axis
        """
        return 1.0 * self.y_max / self.image_height

    def width(self) -> int:
        """
        :return: Width of the bounding box
        """
        return self.x_max - self.x_min
