import os
import xml.etree.ElementTree as ET

def createFile():
    parentPath = os.path.normpath(os.getcwd() + os.sep + os.pardir) #./VideoExtractionServer
    os.chdir(parentPath)
    f = open("./data/final_dataset_lego_detection/trainingData.txt", "w")
    return f

def writeToFile(trainingDataFile, annotation):
    if annotation != "":
        trainingDataFile.write(annotation + "\n")

def findClassNameIndex(className):
    file = open("./data/final_dataset_lego_detection/classes.txt", "r")
    index = 0
    for line in file:
        if line != className:
            index += 1
        else:
            file.close()
            return index

def getValues(root, trainingDataFile, annotation, classIndex, directory):
    pathToFiles = '/data/final_dataset_lego_detection/photos/'

    for elem in root:
        if elem.text != None:
            if elem.tag == "filename":
                annotation += pathToFiles + directory + '/' + elem.text + ' '
            elif elem.tag == "xmin":
                annotation += elem.text + ','
            elif elem.tag == "ymin":
                annotation += elem.text + ','
            elif elem.tag == "xmax":
                annotation += elem.text + ','
            elif elem.tag == "ymax":
                annotation += elem.text + ',0 '
            elif elem.tag == "name":
                classIndex = findClassNameIndex(elem.text)
            annotation, classIndex = getValues(elem, trainingDataFile, annotation, classIndex, directory)
    return annotation, classIndex

if __name__ == '__main__':

    trainingDataFile = createFile();

    path = './data/final_dataset_lego_detection/photos'
    files = []

    for directory in os.listdir(path):
        directoryPath = path + '/' + directory
        for file in os.listdir(directoryPath):
            singleFilePath = directoryPath + '/' + file
            fileName, fileExtension = os.path.splitext(singleFilePath)
            if fileExtension == ".xml":
                tree = ET.parse(singleFilePath)
                root = tree.getroot()

                annotation = ""
                classIndex = 0
                data, classIndex = getValues(root, trainingDataFile, annotation, classIndex, directory)
                writeToFile(trainingDataFile, data) # write to file in format: path, xmin, ymin, xmax, ymax, classIndex

    trainingDataFile.close();















