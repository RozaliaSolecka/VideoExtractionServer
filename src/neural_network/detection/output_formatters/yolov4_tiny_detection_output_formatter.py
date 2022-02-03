from typing import List

import tensorflow as tf

from .i_detection_output_formatter import IDetectionOutputFormatter
from model.detected_output import DetectedOutput


class YoloV4TinyDetectionOutputFormatter(IDetectionOutputFormatter):
    __number_of_classes = 1

    def format(self, base_output, image_w, image_h) -> List[DetectedOutput]:
        for key, value in base_output.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=0.45,
            score_threshold=0.55
        )
        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        out_boxes, out_scores, out_classes, num_boxes = pred_bbox

        output_list = []
        for i in range(num_boxes[0]):
            if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > self.__number_of_classes:
                continue
            coordinate = out_boxes[0][i]
            y_min = int(coordinate[0] * image_h)
            y_max = int(coordinate[2] * image_h)
            x_min = int(coordinate[1] * image_w)
            x_max = int(coordinate[3] * image_w)
            score = out_scores[0][i]
            score = round(score * 100, 2)
            output = DetectedOutput(x_min, y_min, x_max, y_max, score, image_w, image_h)
            output_list.append(output)
        return output_list
