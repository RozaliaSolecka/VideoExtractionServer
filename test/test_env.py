from unittest import TestCase

try:
    import numpy as np
except:
    pass
try:
    import tensorflow as tf
except:
    pass
try:
    import PIL
except:
    pass
try:
    import cv2
except:
    pass


class TestEnvironment(TestCase):
    def test_numpy(self):
        result = np.__version__
        self.assertGreater(len(result), 0)

    def test_tensorflow(self):
        result = tf.__version__
        self.assertGreater(len(result), 0)

    def test_pillow(self):
        result = PIL.__version__
        self.assertGreater(len(result), 0)

    def test_opencv(self):
        result = cv2.__version__
        self.assertGreater(len(result), 0)
