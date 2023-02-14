import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
# from mainwindow_menu import Window


class Close(QtGui.QDialog):
    def __init__(self, rightpane=None):
        super(Close, self).__init__()
        self.rightpane = rightpane
        self.setWindowTitle("System Search Hub")
        self.labelWarn  = QtGui.QLabel("Exit SSH ?")
        self.buttonYes  = QtGui.QPushButton('Yes', self)
        self.buttonYes.clicked.connect(self.handleYes)
        self.buttonNo   = QtGui.QPushButton('No', self)
        self.buttonNo.clicked.connect(self.handleNo)

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.labelWarn, 0, 1)
        layout.addWidget(self.buttonYes, 1, 0)
        layout.addWidget(self.buttonNo,  1, 2)


    def handleYes(self):
        print("close.py,    try to close .................................")
        #self.rightpane.msg_sender("group", "exit")
        #self.rightpane.sock.close()
        self.rightpane.receiver.exit(0)
        exit()


    def handleNo(self): 
        self.accept()



if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    login = Close()

    if login.exec_() == QtGui.QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())

