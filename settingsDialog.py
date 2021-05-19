import sys
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui

class settingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        ## window settings
        self.setWindowTitle("Configuration")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        QBtn = QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel

        

        # labels
        lbl_GSlocation = QtWidgets.QLabel("ghostscript location:")

        # editable text
        txt_gsLocation = QtWidgets.QLineEdit("")

        # buttons
        btn_gsLocation = QtWidgets.QPushButton("Browse")

        # key bindings
        btn_gsLocation.clicked.connect(self.selectGSLocation)

        # button box
        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # create layout and add elements
        self.layout = QtWidgets.QGridLayout(self)
        
        self.layout.addWidget(lbl_GSlocation,0,0)
        self.layout.addWidget(txt_gsLocation,0,1)
        self.layout.addWidget(btn_gsLocation,0,2)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        ## set widget size
        self.setFixedSize(600,400)

        self.readSettings()


    def selectGSLocation(self):
        gsLocation = QtWidgets.QFileDialog.getOpenFileName(self, "Browse for ghostscript", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.HomeLocation), "*.exe")
        self.txt_gsLocation.setText(gsLocation[0])


    def writeSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")
        settings.setValue("gsLocation", "10")
        settings.sync()


    def readSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")


    # this is called when the application is closed
    def closeEvent(self, event):
        self.writeSettings()
        event.accept()