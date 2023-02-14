import matplotlib.pyplot as plt
import numpy as np


class FillBetweenCurves:
    def __init__(self):
        i = 1

    def plot_fill_between_curves(self, plotname, x, y1, y2):


        # now fill between y1 and y2 where a logical condition is met.  Note
        # this is different than calling
        #   fill_between(x[where], y1[where],y2[where]
        # because of edge effects over multiple contiguous regions.
        fig, (ax) = plt.subplots(1, 1, sharex=True)

        ax.plot(x, y1, x, y2, color='black')

        ax.fill_between(x, y1, y2, where=y2 >= y1, facecolor='green', interpolate=True)
        ax.fill_between(x, y1, y2, where=y2 <  y1, facecolor='red',   interpolate=True)
        ax.set_title(plotname)

        plt.show()


if __name__=="__main__": 
    x  = np.arange(0.0, 2, 0.01)
    y1 = np.sin(2*np.pi*x)
    y2 = 1.2*np.sin(4*np.pi*x)

    fillbw = FillBetweenCurves()
    fillbw.plot_fill_between_curves("fill between", x, y1, y2)



