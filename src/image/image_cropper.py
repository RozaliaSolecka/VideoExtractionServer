from typing import List

from numpy import ndarray

from .i_image_cropper import IImageCropper


class ImageCropper(IImageCropper):
    def format(self, images, bounding_boxes) -> List[ndarray]:
        crop_img_list = []
        for i in range(len(bounding_boxes)):
            crop_img = images[bounding_boxes[i].y_min:bounding_boxes[i].y_max,
                       bounding_boxes[i].x_min:bounding_boxes[i].x_max]

            crop_img_list.append(crop_img)
        return crop_img_list
