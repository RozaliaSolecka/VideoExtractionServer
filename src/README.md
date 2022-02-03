# App configuration
App configuration is available by default in `config.ini` file. However, other configuration can be used with `-c` terminal option when starting the application. For example, `python program.py -c another_config.ini` would use `another_config.ini` file as a config.

The commented structure of such configuration is presented below (comments are in lines between triple quotes, before each option):

```
[APP]
"""
This flag allow to choose the type of processing. 
False means processing for the videos.
True allows processing of the photos in single folder.
"""
picture = False         

[CLASSIFIER]
"""
Path to the model weights for the classifier.
"""
model_path = ../model/keras_model/447_classes.h5

[DETECTOR]
"""
Path to the model weights for the detector.
"""
model_path = ../model/yolov4-tiny-lego
"""
Flag indicating the type of the detector's model
False uses yolov4-tiny model using TensorFlow library.
True setting is for using YOLOv5 models used with PyTorch library.
"""
use_yolo_v5 = False

"""
Section available for image processing
"""
[PHOTO]
"""
Path to the folder with images to process.
"""
path = ../data/obj

"""
Section available for video processing 
"""
[VIDEO]
"""
Indicates the length of the break between subsequent classifications. That means that if 1 value is set, then the break will be 1 frame long, so every second frame with detected object could potentially be classified.
"""
classifier_interval_break = 1
"""
This setting allows to adjust the understanding of the distance between next objects. It works this way when set to 3: if 3 consecutive frames does not contain any object, then system decides that next detected object will be the new one, which means it will get the new id. 
"""
empty_frames_limit = 3
"""
Sets the number of frames sent per second by process which reads the video stream.
"""
fps = 30
"""
Indicates number of max classification for object visible on consecutive frames. Setting it to 7 means that after 7 classifications for single physical LEGO brick, the final result for this object will be created, even if it is still visible for the system.
"""
max_number_of_classifications = 7
"""
Setting this flag to true enables video stream mock, which sends single frame with single brick for about 900 times. It allows to make benchmark testing easier, if it is set with max_number_of_classifications with number larger than 900. This way processing will make detections and configured classifications for all fake frames.
"""
benchmark_mock = False
"""
File ath to the video.
"""
path = ../data/Plates_narrow-02.mp4
"""
Setting this to true enables saving the frames from different stages of processing inside output folder. If set to true, then base frames are saved inside original_frames subfolder, detected objects are saved inside detected_objects, and classified object are saved inside classification_results.
"""
save_debug_frames = False
```

It is worth to mention that all file paths should be either full paths or paths relative to this `src` folder.


# Understanding the results

## Photo processing
Every object detected on the photos inside set folder is saved as image inside `output/classified_frames` with name indicating the file, object index and its predicted class. They are called in format `10firstLettersOfSourceFile___indexInImage_predictedLabel.img`.

## Video processing
The system can correctly work with video which contain bricks moving from the right side of the video to the left to properly get correlations between subsequent frames. Without setting `save_debug_frames` flag, the only results are logs: results.log and times.log. Both those log files are cleared on application start. Additionally, setting the mentioned flag also leads to saving images after each processing stage.

### results.log
Contains final results for each object, which is ideally based on multiple classifications, with exact value set in config file. An example log entry is presented below: 

```
2021-12-04 20:18:46,299 [INFO] Object 2 result class: 30363. Position: {
    "last_position_timestamp": "2021-12-04 20:18:46.126",
    "last_position_x": 0.23411458333333335,
    "last_position_y": 0.4550925925925926
}
2021-12-04 20:18:46,299 [DEBUG] ('30363', "Counter({'30363': 3})")
```

INFO entry has final clean results which consists of the object ID, its class, and last position known to the system with its timestamp. A message with such information could be potentially used to inform an external sorting system. The second DEBUG shows the results of single classifications used for the final results in form of the dictionary. In this example, three predictions were performed, and all of them indicated `30363` as correct label.

### times.log
This log file contains mostly information about timing of actions inside the app. It contains timing for events like sending the new frame, getting the frame and passing it to detection, sending object to classification or receiving classification result. It also presents the information on how long it took to detect or classify each frame. In general, this files allows tracing the processing of all frames, which can be useful while we have all frames saved to look at.

Moreover, this file is important to keep track of buffering state of the application. In situations when app cannot handle configured options, then this log also presents ERROR entries describing one of two possible reasons.

The log entry presented below informs that frames are being buffered for classification step, which means that the system cannot handle such frequency of classifications. In such situations in order to allow smooth, on time processing it is required to reduce the interval between consecutive classifications or fps setting, reducing frequency of incoming frames. Both those actions can be done through config file.
```
2021-12-04 19:21:15,946 [ERROR] [VIDEO_SERVICE] Classification result is more than 10 frames late, so classification is too slow for this number of frames per second! Try to reduce number of frames which are classified!
``` 

Another type of entries informs about too frequent incoming frames. To keep things without significant buffering, it is required to reduce the fps option inside config, so fewer frames per second are incoming to the main video service component.
```
2021-12-04 20:31:36,635 [ERROR] [VIDEO_SERVICE] Video queue is bigger than 3, so detection is too slow for this number of frames per second! Try to reduce number of frames per second!
```

### Saved images
There are three folders where frames can be saved from three different stages of processing.

`original_frames` folder contains frames directly from the stream which are named with format `frameIndex.jpg`, e.g. file `20.jpg` would contain a frame with index 20.

`detected_frames` folder contains all objects detected by the system. Each image is saves in cropped form and named `frameIndex_indexWithinImage.jpg`, e.g. file `20_2.jpg` would show the third object detected on `20` frame.

Last folder named `classified_frames` contains object which were classified. This time image is named with format `frameIndex____indexWithinImage_predictedLabel.jpg`, so for example, file `20___0_61409.jpg` presents the first classified object from frame `20` with its predicted label for this cropped image.


# Most important files

## Entry points
The program starts with `program.py` file, which only loads the configuration and calls the MainController from `controllers/main_controller.py` file. This controller invokes service for the configured type of processing. So the real processing starts in `services/photo_service.py` for image processing or inside class in `services/video_service.py` file.

## Place for adding external incoming video stream
Currently, video is provided from additional process which is using VideoRemote from `remotes/video_remote.py` file. It contains `video` function which could be potentially redone to read the stream from an external system. Such handling could then put single frames into a multiprocessing queue which is available there. Main processing would not require any changes as along as the same queue is filled with the frames. This VideoRemote works in different process, so it should not interfere with main processing anyway.

## Place for sending result messages to external system
Presenting the final results is done inside `finishObject` method inside `ResultsService` from file `services/video/results_service.py`. So an advised way of sending external messages would be to call, from this place, a new service handling external connection. Ideally such call should be in asynchronous manner with only delegating the call, so it won't block the main processing loop. 


# Contact
In case of any uncertainties about these explanations or additional questions, please contact, through email, the author of this README file: t.piechocki@yahoo.com ([@TPiechocki at GitHub](https://github.com/TPiechocki))