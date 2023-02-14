# override the default reporting of coords

import matplotlib.pyplot as plt
import numpy as np


class ScatterDots:
    def __init__(self):
        i = 1

    def plot_scatter_dots(self, x, y): 
        fig, ax = plt.subplots()
        plt.plot(x, y, 'o')
        plt.show()


if __name__=="__main__":
    x = np.random.rand(20) 
    y = np.random.rand(20)

    dots = ScatterDots()
    dots.plot_scatter_dots(x, y)


