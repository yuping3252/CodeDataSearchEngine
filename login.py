

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtCore import *
 

# A QDialog has its own event loop, so it can be run separately from the main application.
# So you just need to check the dialog's return code to decide whether the main application should be run or not.
# Example code:
from mainwindow_menu import Window

class Login(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

        self.setWindowTitle("Data Tracing")
        self.labelName    = QtGui.QLabel("User Name")
        self.labelPass    = QtGui.QLabel("User Password")
        self.textName     = QtGui.QLineEdit(self)
        self.textPass     = QtGui.QLineEdit(self)
        self.buttonLogin  = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonCancel = QtGui.QPushButton('Cancel', self)
        self.buttonCancel.clicked.connect(self.handleCancel)

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.labelName, 0, 0)
        layout.addWidget(self.labelPass, 1, 0)
        layout.addWidget(self.textName,  0, 1)
        layout.addWidget(self.textPass,  1, 1)
        layout.addWidget(self.buttonLogin,  2, 0)
        layout.addWidget(self.buttonCancel, 2, 1)

        self.textName.setFocus()
        self.connect(self.textName, SIGNAL('returnPressed()'), self.nameEntered)
        self.connect(self.textPass, SIGNAL('returnPressed()'), self.passEntered)

    def nameEntered(self):
        self.textPass.setFocus()

    def passEntered(self):
        self.handleLogin()

    def handleLogin(self):
        if self.textName.text() != "" and self.textPass.text() != "":
            if (self.textName.text() == 'a' and
                self.textPass.text() == 'b'):
                self.accept()
            else:
                QtGui.QMessageBox.warning(
                    self, 'Error', 'Bad user or password')
                self.textName.clear()
                self.textPass.clear()
                self.textName.setFocus()

    def handleCancel(self):
        exit()

if __name__ == '__main__': 
    import sys
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    login = Login() 
    if login.exec_() == QtGui.QDialog.Accepted:
        window = Window()
        window.show()
        sys.exit(app.exec_())
 
