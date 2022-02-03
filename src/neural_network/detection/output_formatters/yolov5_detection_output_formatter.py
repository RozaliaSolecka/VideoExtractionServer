from typing import List

import numpy as np

from model.detected_output import DetectedOutput
from .i_detection_output_formatter import IDetectionOutputFormatter


class YoloV5DetectionOutputFormatter(IDetectionOutputFormatter):
    __number_of_classes = 1

    def format(self, results, image_w, image_h) -> List[DetectedOutput]:
        image_predictions = results.xyxyn[0].cpu().numpy()
        scores = image_predictions[:, 4]
        classes = image_predictions[:, 5].astype(np.int64) + 1
        boxes = np.array([[coord[1], coord[0], coord[3], coord[2]] for coord in image_predictions[:, :4]])

        output_list = []
        for i in range(len(boxes)):
            if int(classes[i]) < 0 or int(classes[i]) > self.__number_of_classes:
                continue
            coordinate = boxes[i]
            y_min = int(coordinate[0] * image_h)
            y_max = int(coordinate[2] * image_h)
            x_min = int(coordinate[1] * image_w)
            x_max = int(coordinate[3] * image_w)
            score = scores[i]
            score = round(score * 100, 2)
            output = DetectedOutput(x_min, y_min, x_max, y_max, score, image_w, image_h)
            output_list.append(output)
        return output_list
