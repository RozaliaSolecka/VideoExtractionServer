import xlsxwriter
from scripts.training_effectiveness.statistics import GlobalStatistics
from scripts.training_effectiveness.chart import Chart
from scripts.training_effectiveness.chart import ChartElement


class XlsxFile:
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('Statistics.xlsx')
        self.worksheet = self.workbook.add_worksheet()
        self.row = 0
        self.column = 0
        self.chart = Chart()
        self.chart_element = ChartElement()


        title = (
            ['Directory', 'number of objects', 'number of detected objects', 'number of correctly recognized objects',
             'percentage of correctly recognised', 'number of photos']
        )
        # Iterate over the data and write it out row by row.
        for item in (title):
            self.worksheet.write(self.row, self.column, item)
            self.column += 1
        self.row += 1
        self.column = 0

    def add_row(self, global_statistics : GlobalStatistics):
        number_of_objects = global_statistics.number_of_objects_for_directory
        number_of_found_objects = global_statistics.number_of_found_objects_for_directory
        number_of_correctly_recognised = global_statistics.number_of_correctly_recognised_for_directory
        percentage_of_correctly_recognised = global_statistics.percentage_of_correctly_recognised_for_directory
        number_of_files = global_statistics.number_of_files_for_directory

        new_row = [number_of_objects, number_of_found_objects, number_of_correctly_recognised,
                   percentage_of_correctly_recognised, number_of_files]

        if new_row[0] != 0: # skip directories with only names
            self.worksheet.write(self.row, self.column, global_statistics.file)
            self.column += 1
            for item in (new_row):
                self.worksheet.write(self.row, self.column, item)
                self.column += 1
            self.row += 1
            self.column = 0

            self.chart_element.dictionary = global_statistics.file
            self.chart_element.number_of_objects = new_row[0]
            self.chart_element.number_of_detected_objects = new_row[1]
            self.chart_element.number_of_correctly_recognised_objects = new_row[2]
            self.chart_element.percentage_of_correctly_recognised = new_row[3]
            self.chart.append_element_to_list(self.chart_element)

    def close_workbook(self):
        self.workbook.close()
        self.chart.chart()  # draw chart