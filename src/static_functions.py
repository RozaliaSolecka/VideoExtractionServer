import json
import os
import shutil
from typing import List

import cv2
from numpy import ndarray

from neural_network.classification.classification_results import ClassificationResults


def read_class_names(class_file_name):
    names = {}
    with open(class_file_name, 'r') as data:
        for ID, name in enumerate(data):
            names[ID] = name.strip('\n')
    return names


def prepare_frames_folder(output_path):
    clear_folder(output_path + "/original_frames")
    clear_folder(output_path + "/detected_frames")
    clear_folder(output_path + "/classified_frames")


def clear_folder(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    os.mkdir(path)


def save_original_frame(frame: ndarray, counter: int) -> None:
    folder_path = '../output/original_frames/' + \
                  str(counter) + '.jpg'
    cv2.imwrite(folder_path, frame)


def save_detected_photos(crop_img_list: List[ndarray], counter: int) -> None:
    i = 0
    for crop_img in crop_img_list:
        folder_path = '../output/detected_frames/' + \
                      str(counter) + '_' + \
                      str(i) + '.jpg'
        cv2.imwrite(folder_path, crop_img)
        i += 1


def save_classified_photos(crop_img_list: List[ndarray], classification_results: ClassificationResults,
                             filename_base: any) -> None:
    i = 0
    for crop_img in crop_img_list:
        folder_path = '../output/classified_frames/' + \
                      str(filename_base) + '___' + \
                      str(i) + '_' + \
                      str(classification_results.classification_classes[i]) + '.jpg'
        cv2.imwrite(folder_path, crop_img)
        i += 1


def toJSON(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)
