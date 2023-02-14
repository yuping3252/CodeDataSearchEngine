"""
===============
Basic pie chart
===============

Demo of a basic pie chart plus a few additional features.

In addition to the basic pie chart, this demo shows a few optional features:

    * slice labels
    * auto-labeling the percentage
    * offsetting a slice with "explode"
    * drop-shadow
    * custom start angle

Note about the custom start angle:

The default ``startangle`` is 0, which would start the "Frogs" slice on the
positive x-axis. This example sets ``startangle = 90`` such that everything is
rotated counter-clockwise by 90 degrees, and the frog slice starts on the
positive y-axis.
"""
import matplotlib.pyplot as plt

# Pie chart, where the slices will be ordered and plotted counter-clockwise:



class PieChart:
    def __init__(self):
        i = 1

    def plot_piechart(self, labels, sizes): 
        labels_distinct, sizes_accum_amt = self.distinct_labels(labels, sizes)

        explode = []
        for i in range(len(labels_distinct)):
            explode.append(0)
        fig1, ax1 = plt.subplots() 
        ax1.pie(sizes_accum_amt, explode=explode, labels=labels_distinct, autopct='%1.1f%%',
        shadow=True, startangle=90) 
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.show()


    def distinct_labels(self, labels, sizes):
        l_distinct = []
        s_distinct = []

        p = 0
        for d in labels:
            if l_distinct.count(d) == 0: 
                l_distinct.append(d)
                s_distinct.append(p)
            p += 1

        s_accum_amt = []

        for l_ in l_distinct:
            s_amt = 0
            s_pos = 0

            for l in labels:
                if l_ == l:
                    s_amt += sizes[s_pos]
                s_pos += 1
            s_accum_amt.append(s_amt)

        s_total = 0
        for a in s_accum_amt:
            s_total += a

        s_accum_amt2 = []
        for a in s_accum_amt:
            s_accum_amt2.append(a/s_total)

        return l_distinct, s_accum_amt2




if __name__=="__main__": 
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    pie = PieChart()
    pie.plot_piechart(labels, sizes)
