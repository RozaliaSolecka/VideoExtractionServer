import matplotlib
import matplotlib.pyplot as plt
import copy
import operator

class ChartElement:
    def __init__(self):
        self.dictionary = ""
        self.number_of_objects = 0
        self.number_of_detected_objects = 0
        self.number_of_correctly_recognised_objects = 0
        self.percentage_of_correctly_recognised = 0

class Chart:
    def __init__(self):
        self.chart_elements = []

        self.dictionaries = []
        self.percentages_of_correctly_recognised = []

        self.dictionaries_over_100_percent = []
        self.numbers_of_objects_over_100_percent = []
        self.numbers_of_detected_objects_over_100_percent = []
        self.numbers_of_correctly_recognised_objects_over_100_percent = []

        self.y_min = 90
        self.y_max = 100
        self.threshold_min = []
        self.threshold_max = []

    def append_element_to_list(self, chart_element: ChartElement):
        ce = copy.copy(chart_element)
        self.chart_elements.append(ce)

    def chart(self):
        self.chart_elements.sort(key=operator.attrgetter('percentage_of_correctly_recognised'))
        for e in self.chart_elements:
            self.dictionaries.append(e.dictionary)
            self.percentages_of_correctly_recognised.append(e.percentage_of_correctly_recognised)
            self.threshold_min.append(self.y_min)
            self.threshold_max.append(self.y_max)

            if e.percentage_of_correctly_recognised > 100:
                self.dictionaries_over_100_percent.append(e.dictionary)
                self.numbers_of_objects_over_100_percent.append(e.number_of_objects)
                self.numbers_of_detected_objects_over_100_percent.append(e.number_of_detected_objects)
                self.numbers_of_correctly_recognised_objects_over_100_percent.append(e.number_of_correctly_recognised_objects)

        plt.plot(self.dictionaries, self.percentages_of_correctly_recognised, 'o', mfc='none', label="Różne rodzaje klocków")
        plt.plot(self.dictionaries, self.threshold_min, '-', label='y='+str(self.y_min))
        plt.plot(self.dictionaries, self.threshold_max, '-', label='y='+str(self.y_max))
        plt.legend(loc="lower right", fontsize=20)
        plt.xticks([])
        plt.yticks(fontsize=20)
        #plt.title('Skuteczność działania detekcji', fontsize=20)
        plt.xlabel('Rodzaj klocka', fontsize=20 )
        plt.ylabel('Procent poprawnie wykrytych klocków [%]', fontsize=20)
        plt.show()
        # plt.savefig('detection_effectiveness.png')

        plt.plot(self.dictionaries_over_100_percent, self.numbers_of_objects_over_100_percent, 'o', mfc='none', label = "Liczba klocków")
        plt.plot(self.dictionaries_over_100_percent, self.numbers_of_detected_objects_over_100_percent, 'o', mfc='none',  label = "Liczba wykrytych obiektów")
        plt.plot(self.dictionaries_over_100_percent, self.numbers_of_correctly_recognised_objects_over_100_percent, 'o', mfc='none', label = "Liczba poprawnie wykrytych klocków")
        plt.legend(loc="upper right", fontsize=20)
        plt.grid()
        ax = plt.gca()
        ax.axes.xaxis.set_ticklabels([])
        plt.yticks(fontsize=20)
        #plt.title('Otrzymane wyniki, gdy procent poprawnie wykrytch obiektów jest większy niż 100%', fontsize=20)
        plt.xlabel('Rodzaj klocka', fontsize=20)
        plt.ylabel('Liczba obiektów', fontsize=20)
        plt.show()
        # plt.savefig('results_over_100_percent.png')








