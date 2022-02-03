from copy import deepcopy

from scripts.training_effectiveness.math import IoU
from scripts.training_effectiveness.record import Record


class DataFile:
    def __init__(self):
        self.records = []

    def check_number_of_objects(self):
        return len(self.records)

    def check_if_correctly_recognised(self, file, error_rate):
        number_of_correctly_recognised = 0

        for record_in in self.records:
            for record_out in file.records:
                iou = IoU(record_in, record_out)

                if iou > error_rate:
                    number_of_correctly_recognised += 1

        return number_of_correctly_recognised

    def assign_values_to_record_object(self, lines):
        rec = Record()  # single row with data in file

        for line in lines:
            if line != '\n':
                values = line.split()
                rec.class_number = values[0]
                rec.x_center = values[1]
                rec.y_center = values[2]
                rec.width = values[3]
                rec.height = values[4]
                rec.determine_coordinates()
                self.records.append(deepcopy(rec))

    def assign_values_to_record_object_with_filtering(self, lines):
        rec = Record()  # single row with data in file

        for line in lines:
            if line != '\n':
                values = line.split()
                rec.class_number = values[0]
                rec.x_center = values[1]
                rec.y_center = values[2]
                rec.width = values[3]
                rec.height = values[4]
                rec.determine_coordinates()

                if not (rec.x_l < 0.01 or rec.x_r < 0.01 or rec.y_d < 0.01 or rec.y_u < 0.01 or rec.x_l > 0.99 or \
                        rec.x_r > 0.99 or rec.y_d > 0.99 or rec.y_u > 0.99):
                    self.records.append(deepcopy(rec))
