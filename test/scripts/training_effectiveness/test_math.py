from unittest import TestCase

from scripts.training_effectiveness.math import IoU
from scripts.training_effectiveness.record import Record


class TestIoU(TestCase):
    def test_IoU(self):
        test_cases = [
            ((400, 600, 400, 600, 200, 200), (400, 600, 400, 600, 200, 200), 1),
            ((.4, .6, .4, .6, .2, .2), (.4, .6, .4, .6, .2, .2), 1),
            ((.25, .44, .21, .39, .19, .18), (.28, .438, .19, .39, .158, .2), .76)
        ]

        for test_case in test_cases:
            record = Record()
            record.x_l, record.x_r, record.y_u, record.y_d, record.width, record.height = test_case[0]

            other = Record()
            other.x_l, other.x_r, other.y_u, other.y_d, other.width, other.height = test_case[1]

            self.assertAlmostEqual(IoU(record, other), test_case[2], 2)
