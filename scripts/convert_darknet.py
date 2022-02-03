import os
import sys
import xml.etree.ElementTree as ET


def createFile(file_path):
    f = open(file_path, "w")
    return f


def writeToFile(training_data_file, annotation):
    if annotation != "":
        training_data_file.write(annotation + "\n")


def getValues(root, width, height, x_min, y_min, x_max, y_max, annotation):
    for elem in root:
        if elem.text is not None:
            if elem.tag == "width":
                width = int(elem.text)
            elif elem.tag == "height":
                height = int(elem.text)
            elif elem.tag == "xmin":
                x_min = int(elem.text)
            elif elem.tag == "ymin":
                y_min = int(elem.text)
            elif elem.tag == "xmax":
                x_max = int(elem.text)
            elif elem.tag == "ymax":
                y_max = int(elem.text)

                x_center = int(x_max + x_min) / 2 / width
                y_center = int(y_max + y_min) / 2 / height
                w = int(x_max - x_min) / width
                h = int(y_max - y_min) / height
                # 0 is class identifier
                annotation += '0 ' + str(x_center) + ' ' + str(y_center) + ' ' + str(w) + ' ' + str(h) + '\n'

            width, height, x_min, y_min, x_max, y_max, annotation = getValues(elem, width, height, x_min, y_min, x_max, y_max,
                                                                              annotation)
    return width, height, x_min, y_min, x_max, y_max, annotation


def annotate(start_path):
    """
    Creates .txt files for each .xml (.jpg) file
    :param start_path: path where recursive operation starts
    """
    for file in os.listdir(start_path):   #
        newPath = start_path + '/' + file

        if os.path.isdir(newPath):      # if is directory, than recursive call
            annotate(newPath)
        else:   # process file
            fileName, fileExtension = os.path.splitext(newPath)
            if fileExtension == ".xml":     # describe xml files in additional text file
                tree = ET.parse(newPath)
                root = tree.getroot()

                fileToCreate = fileName + '.txt'    # fileName contains path
                fileToWrite = createFile(fileToCreate)

                annotation = ""
                w = h = xmin = ymin = xmax = ymax = 0

                width, height, x_min, y_min, x_max, y_max, data = getValues(root, w, h, xmin, ymin, xmax, ymax,
                                                                            annotation)

                writeToFile(fileToWrite, data)
                fileToWrite.close()


def listFiles(start_path, output_file):
    """
    Fill file with names of all .jpg files
    :param start_path: path where recursive searching of .jpg files starts
    :param output_file: File where listed files are saved.
    """
    for file in os.listdir(start_path):
        newPath = start_path + '/' + file

        if os.path.isdir(newPath):  # if is directory, than recursive call
            listFiles(newPath, output_file)
        else:   # process file
            singleFilePath = start_path + '/' + file
            fileName, fileExtension = os.path.splitext(singleFilePath)
            if fileExtension == ".jpg":     # write path if file is jpeg photo
                writeToFile(output_file, singleFilePath)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("You need to specify single path argument")
        exit(1)

    path = sys.argv[1]

    annotate(path)

    trainFile = createFile("./train.txt")
    listFiles(path, trainFile)
