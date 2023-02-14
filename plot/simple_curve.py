
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure                  import Figure                                      # a figure to plot on
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg    as FigureCanvas        # canvas holds a figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar   # navigation links to a canvas






class SimpleCurve(QDialog):
    def __init__(self, parent=None):
        super(SimpleCurve, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot_simple_curve)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.show()


    def plot_simple_curve(self, t_nm, t, s_nm, s): 
        plt.plot(t, s)

        plt.xlabel('time (s)')
        plt.ylabel('voltage (mV)')
        plt.title('About as simple as it gets, folks')
        plt.grid(True)
        plt.savefig("test.png")


        plt.xlabel(t_nm)
        plt.ylabel(s_nm)
        plt.xticks(rotation=70)

        self.canvas.draw()
        plt.show()


if __name__=="__main__": 
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2*np.pi*t)
    simple = SimpleCurve()
    simple.plot_simple_curve(t, s)
