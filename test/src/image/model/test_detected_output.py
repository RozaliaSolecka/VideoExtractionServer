from unittest import TestCase

from src.model.detected_output import DetectedOutput


class TestRelativeCenter(TestCase):
    relative_center_test_cases = [
        (100, 300, 700, 1 - 2.0 / 7),
        (400, 800, 800, .25)
    ]

    def test_should_return_correct_x_relative_center(self):
        for (x_min, x_max, width, expectedResult) in self.relative_center_test_cases:
            sut = DetectedOutput(x_min, 0, x_max, 0, 0, width, 0)

            result = sut.relative_center_x()

            self.assertAlmostEqual(result, expectedResult, 4)

    def test_should_return_correct_y_relative_center(self):
        for (y_min, y_max, height, expectedResult) in self.relative_center_test_cases:
            sut = DetectedOutput(0, y_min, 0, y_max, 0, 0, height)

            result = sut.relative_center_y()

            self.assertAlmostEqual(result, expectedResult, 4)

    relative_coordinate_test_cases = [
        (100, 1000, .1),
        (300, 900, 1.0/3)
    ]

    def test_should_return_correct_x_min(self):
        for (x, width, expectedResult) in self.relative_coordinate_test_cases:
            sut = DetectedOutput(x, 0, 0, 0, 0, width, 0)

            result = sut.relative_x_min()

            self.assertAlmostEqual(result, expectedResult, 4)

    def test_should_return_correct_x_max(self):
        for (x, width, expectedResult) in self.relative_coordinate_test_cases:
            sut = DetectedOutput(0, 0, x, 0, 0, width, 0)

            result = sut.relative_x_max()

            self.assertAlmostEqual(result, expectedResult, 4)
