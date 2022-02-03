import os
import sys

from scripts.training_effectiveness.data_file import DataFile
from scripts.training_effectiveness.statistics import Statistics, GlobalStatistics
from scripts.training_effectiveness.xlsx_file import XlsxFile

error_rate = 0.5

def create_file(file_path):
    f = open(file_path, "w")
    return f

def make_statistics(data_file_in, data_file_out, statistics_file_path, global_statistics: GlobalStatistics):
    statistic = Statistics()

    statistic.number_of_objects = data_file_in.check_number_of_objects()
    statistic.number_of_found_objects = data_file_out.check_number_of_objects()
    statistic.number_of_correctly_recognised = data_file_in.check_if_correctly_recognised(data_file_out, error_rate)

    statistics_file = create_file(statistics_file_path)
    statistics_file.write(str(statistic))
    statistics_file.close()

    global_statistics.add_to_statistics(statistic)

def annotate(start_path_in, global_statistics: GlobalStatistics, xlsx_file):
    """
    Creates .txt files for each pair of .txt files compared
    :param global_statistics: statistics for the whole dataset
    :param start_path_in: path where recursive operation starts in input data
    """

    for file in os.listdir(start_path_in):  #
        new_path = start_path_in + '\\' + file

        fileName, fileExtension = os.path.splitext(new_path)
        if fileExtension == '.txt':
            global_statistics.set_number_of_files()  # how many .txt files in annotation

        if os.path.isdir(new_path):  # if is directory, than recursive call
            if file != "PART_1" and file != "PART_2" and file != "PART_3":
                annotate(new_path, global_statistics, xlsx_file)
                global_statistics.file = file
                xlsx_file.add_row(global_statistics)
                global_statistics.clear_statistics_for_directory()
            else:
                annotate(new_path, global_statistics, xlsx_file)
        else:  # process file

            # in_file
            data_file_in = DataFile()
            file_in = open(new_path, 'r')
            lines = file_in.readlines()
            data_file_in.assign_values_to_record_object(lines)
            #data_file_in.assign_values_to_record_object_with_filtering(lines)

            # out_file
            data_file_out = DataFile()
            file_out_path = new_path.replace("annotations", "annotations.lego")
            file_out_path = file_out_path.replace(".txt", ".lego.txt")
            file_out = open(file_out_path, 'r')
            lines = file_out.readlines()
            data_file_out.assign_values_to_record_object(lines)
            #data_file_out.assign_values_to_record_object_with_filtering(lines)

            statistics_file_path = file_out_path.replace(".txt", ".statistics.txt")
            make_statistics(data_file_in, data_file_out, statistics_file_path, global_statistics)

            file_in.close()
            file_out.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("You need to specify single path argument")
        exit(1)

    path_in = sys.argv[1]

    if len(sys.argv) >= 3:
        error_rate = float(sys.argv[2])
        print("Using error rate of " + str(error_rate))

    global_statistics = GlobalStatistics()
    xlsx_file = XlsxFile()

    annotate(path_in, global_statistics, xlsx_file)

    print(global_statistics)
    xlsx_file.close_workbook()