"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt



class BarChartCount:                          # used in tables\table_op.py

    def __init__(self):
        i = 1

    def plot_barchart_cnt(self, x_colnm, x_cols): 
        x_distinct, x_distinct_cnt = self.distinct_data(x_cols)

        n_groups     = len(x_distinct)

        categories   = tuple(x_distinct_cnt)
        std_c_lst    = []
        for i in range(len(x_distinct_cnt)):
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
        plt.ylabel("Count")
        plt.title('')

        plt.xticks(rotation=70)

        x_distinct_label = []
        for x in x_distinct:
            x_distinct_label.append(str(x))
        plt.xticks(index + bar_width / 2, tuple(x_distinct_label))
        # plt.legend()

        plt.tight_layout()
        plt.show()



    def distinct_data(self, xdata):
        x_distinct = []
        c          = 0
        for d in xdata:
            if  x_distinct.count(d) == 0: 
                x_distinct.append(d)
            c += 1

        x_distinct_cnt = []
        for x_ in x_distinct:
            x_cnt = 0
            for x in xdata:
                if x_ == x:
                    x_cnt += 1
            x_distinct_cnt.append(x_cnt)

        return x_distinct, x_distinct_cnt


