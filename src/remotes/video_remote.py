import logging
import string
import time
from datetime import datetime

import cv2
import ray
from ray.util.queue import Queue

from model.video_frame import VideoFrame


@ray.remote(num_cpus=1)
class VideoRemote:
    """
    Async processing of the video and send the frames with constant speed.
    """
    def __init__(self, fps: int):
        """
        :param fps: number of frames per second sent for detection
        """
        self.__fps = fps
        self.__s_interval = 1.0 / self.__fps
        logging.basicConfig(level=logging.INFO, filename='../times.log',
                            filemode='a+', format='%(asctime)s [%(levelname)s] [VIDEO_REMOTE] %(message)s')

    def benchmark_mock(self, queue: Queue):
        """
        Allows to easily mock the order of the frames and send them for detection.
        :param queue: queue used to put images as frames for detection
        """
        image_lego = cv2.imread('../data/obj/0_qZOF_original_3460_1609896037289.jpg')

        images = [image_lego, image_lego, image_lego, image_lego, image_lego, image_lego, image_lego]

        for i in range(7):
            images += images

        counter = 0
        start_time = time.time()
        while len(images):
            logging.info(f"VIDEO FRAME {counter} SENT")
            queue.put(VideoFrame(images.pop(), counter, datetime.now()))
            self.__wait_for_next_frame(start_time)
            counter += 1
            start_time += self.__s_interval

    def video(self, queue: Queue, path: string):
        """
        Processes the video and send frames to the detection.
        :param queue: queue used to put images as frames for detection
        :param path: path of the video
        """
        vid = cv2.VideoCapture(path)
        counter = 0
        start_time = time.time()
        while True:
            return_value, frame = vid.read()
            if not return_value:
                break

            logging.info(f"VIDEO FRAME {counter} SENT")
            queue.put(VideoFrame(frame, counter, datetime.now()))
            self.__wait_for_next_frame(start_time)
            counter += 1
            start_time += self.__s_interval

        vid.release()

    def __wait_for_next_frame(self, start_time):
        if not time.time() - start_time > self.__s_interval:
            time.sleep(self.__s_interval - (time.time() - start_time))
