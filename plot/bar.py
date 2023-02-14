"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import numpy as np
import matplotlib.pyplot as plt


from matplotlib.figure                  import Figure                                      # a figure to plot on
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg    as FigureCanvas        # canvas holds a figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar   # navigation links to a canvas





class Bar(QWidget):             # used in tables\table_op.py, plotpane.py

    def __init__(self):
        super(BarChartAmount, self).__init__()
        i = 1

    def plot_barchart_amt(self, x_colnm, x_col_data, y_colnm, y_col_data): 
        x_distinct, y_accum_amt = self.distinct_data(x_col_data, y_col_data)

        n_groups     = len(x_distinct)

        categories   = tuple(y_accum_amt)
        std_c_lst    = []
        for i in range(len(y_accum_amt)):
            std_c_lst.append(0)
        std_c        = tuple(std_c_lst)

        fig, ax      = plt.subplots()

        index        = np.arange(n_groups)
        bar_width    = 0.25

        opacity      = 0.4
        error_config = {'ecolor': '0.3'}

        rects1 = plt.bar(index, categories, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=std_c,
                 error_kw=error_config,
                 label='')

        plt.xlabel(x_colnm)
        plt.ylabel(y_colnm)
        plt.title('')

        plt.xticks(rotation=70)

        x_distinct_label = []
        for x in x_distinct:
            x_distinct_label.append(str(x))
        plt.xticks(index + bar_width / 2, tuple(x_distinct_label))
        # plt.legend()

        plt.tight_layout()
        plt.show()



    def distinct_data(self, xdata, ydata):
        x_distinct  = []
        x_positions = []

        p = 0
        for d in xdata:
            if  x_distinct.count(d) == 0: 
                x_distinct.append(d)
                x_positions.append(p)
            p += 1

        y_accum_amt = []

        for x_ in x_distinct:
            y_amt = 0
            y_pos = 0
            for x in xdata:
                if x_ == x:
                    y_amt += ydata[y_pos]
                y_pos += 1
            y_accum_amt.append(y_amt)

        return x_distinct, y_accum_amt


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    barchart = Bar()

    barchart.plot_barchart_amt("X axis", [0, 1, 2, 3, 4, 5, 6, 7, 8], "Y axis", [3, 1, 6, 3, 9, 3, 6, 3, 1] )
    barchart.show()
    sys.exit(app.exec_())


