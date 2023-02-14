import sys
import numpy as np
import matplotlib.pyplot as plt

# related modules:  plotpane.py, 


class LineWithBlocks:
    def __init__(self):
        i = 1

    def plot_line_with_blocks(self, xcolnm, x_cols, ycolnm, y_cols):
        fig = plt.figure()
        ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # (x0, y0, width, height)  (x0, y0) lower left corner

        line = ax1.plot(x_cols, y_cols, 'rs-')

        plt.xlabel(xcolnm)
        plt.ylabel(ycolnm)
        plt.title('')
        #plt.xticks(tuple(x), tuple(x)) 

        fig.legend((line), ('Line 1'), loc='upper center', shadow=True)
        plt.show()

if __name__ == "__main__":
    x_cols = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    y_cols = [0.3, 0.1, 0.2, 0.7, 0.5, 0.5, 0.2, 0.7, 0.8, 0.1, 1.0, 0.1, 0.2]
    xcolnm = "XXX"
    ycolnm = "YYY"

    lineplot = LineWithBlocks()
    lineplot.plot_line_with_blocks(xcolnm, x_cols, ycolnm, y_cols)
