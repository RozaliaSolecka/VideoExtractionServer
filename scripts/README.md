## convert.py

###Description: 
This script extracts training data from .xml file and creates specific data format, suitable for network input.

###Files:
- in VideoExtractionServer data subdirectory is created to store final_dataset_lego_detection directory with .xml and .jpg files (VideoExtractionServer\data\final_dataset_lego_detection)
- training data is saved to file called trainingData.txt  (VideoExtractionServer\data\final_dataset_lego_detection\trainingData.txt).
- the class names are in the classes.txt file (VideoExtractionServer\data\final_dataset_lego_detection\classes.txt).

###Paths:
- Path variable specifies the path to the directory, which contains .xml source files. Path is set in code.
- PathToFiles variable specifies the part of the real path to file with .jpg extension. It is used to create path e.g. /data/final_dataset_lego_detection/photos/1/0_1JNv_original_1608915001732.jpg
instead of /home/slawek/Projects/lego/LegoSorterServer/lego_sorter_server/images/storage/stored/original/0_1JNv_original_1608915001732.jpg

## convert_darknet.py

###Description: 
This script extracts training data from .xml file and creates specific data format, suitable for network input.

###Files:
- in VideoExtractionServer data subdirectory is created to store ./obj/photos/nr (nr - integer as a name of directory) with .xml, .jpg, .txt files 
- training data are saved to file called with file name and .txt extension. Each .xml (.jpg) has respondent .txt file with specific data format  (VideoExtractionServer/data/obj/photos/1/0_1JNv_original_1608915001732.txt).
- train.txt file contains paths of all created .txt files.

###Paths:
- Path to data subdirectory is given as parameter.

###Used data: 
https://mostwiedzy.pl/pl/open-research-data/tagged-images-with-lego-bricks,209111650250426-0