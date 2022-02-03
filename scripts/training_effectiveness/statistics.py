class Statistics:
    def __init__(self):
        self.number_of_objects = None
        self.number_of_found_objects = None
        self.number_of_correctly_recognised = None

    def __str__(self) -> str:
        return "number of objects: " + str(self.number_of_objects) + "\n" + \
            "number of detected objects: " + str(self.number_of_found_objects) + "\n" + \
            "number of correctly recognized objects: " + str(self.number_of_correctly_recognised) + "\n"


class GlobalStatistics:
    def __init__(self):
        self.number_of_objects = 0
        self.number_of_found_objects = 0
        self.number_of_correctly_recognised = 0

        self.number_of_objects_for_directory = 0
        self.number_of_found_objects_for_directory = 0
        self.number_of_correctly_recognised_for_directory = 0
        self.percentage_of_correctly_recognised_for_directory = 0
        self.number_of_files_for_directory = 0
        self.file = ""

        self.number_of_files = 0  # number of .txt files

    def add_to_statistics(self, file_statistics: Statistics):
        self.number_of_objects += file_statistics.number_of_objects
        self.number_of_found_objects += file_statistics.number_of_found_objects
        self.number_of_correctly_recognised += file_statistics.number_of_correctly_recognised

        self.number_of_objects_for_directory += file_statistics.number_of_objects
        self.number_of_found_objects_for_directory += file_statistics.number_of_found_objects
        self.number_of_correctly_recognised_for_directory += file_statistics.number_of_correctly_recognised


        if self.number_of_objects_for_directory != 0:
            self.percentage_of_correctly_recognised_for_directory = (
                    round(self.number_of_correctly_recognised_for_directory / self.number_of_objects_for_directory, 4) * 100)
        else:
            self.percentage_of_correctly_recognised_for_directory = None

    def clear_statistics_for_directory(self):
        self.number_of_objects_for_directory = 0
        self.number_of_found_objects_for_directory = 0
        self.number_of_correctly_recognised_for_directory = 0
        self.percentage_of_correctly_recognised_for_directory = 0
        self.number_of_files_for_directory = 0

    def __str__(self) -> str:
        return "number of objects: " + str(self.number_of_objects) + "\n" + \
            "number of detected objects: " + str(self.number_of_found_objects) + "\n" + \
            "number of correctly recognised objects: " + str(self.number_of_correctly_recognised) + "\n" + \
            "percentage of correctly recognised: " \
               + str(round(self.number_of_correctly_recognised / self.number_of_objects, 4) * 100) + "%\n" + \
            "number of files: " + str(self.number_of_files)

    def set_number_of_files(self):
        self.number_of_files += 1
        self.number_of_files_for_directory += 1
