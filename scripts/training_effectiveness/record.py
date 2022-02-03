class Record:
    def __init__(self):
        self.class_number = None
        self.x_center = None
        self.y_center = None
        self.width = None
        self.height = None
        self.x_r = None
        self.x_l = None
        self.y_u = None
        self.y_d = None

    def determine_coordinates(self):  # xA = (x_l, y_u), xB = (x_r, y_d)
        self.x_r = float(self.x_center) + float(self.width) / 2
        self.x_l = float(self.x_center) - float(self.width) / 2
        self.y_u = float(self.y_center) - float(self.height) / 2
        self.y_d = float(self.y_center) + float(self.height) / 2
