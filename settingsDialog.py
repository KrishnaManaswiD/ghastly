import sys
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui

class settingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        ## window settings
        self.setWindowTitle("Configuration")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        # labels
        lbl_GSlocation = QtWidgets.QLabel("ghostscript location:")

        # editable text
        self.txt_gsLocation = QtWidgets.QLineEdit("")

        # buttons
        btn_gsLocation = QtWidgets.QPushButton("Browse")

        # key bindings
        btn_gsLocation.clicked.connect(self.selectGSLocation)

        # check box
        self.chk_shouldShowConfigAtLaunch = QtWidgets.QCheckBox("Show settings at launch")
        self.chk_shouldShowConfigAtLaunch.setChecked(True)

        # button box
        QBtn = QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        # create layout and add elements
        layout = QtWidgets.QGridLayout(self)
        
        layout.addWidget(lbl_GSlocation,0,0)
        layout.addWidget(self.txt_gsLocation,0,1)
        layout.addWidget(btn_gsLocation,0,2)
        layout.addWidget(self.chk_shouldShowConfigAtLaunch,1,0)
        layout.addWidget(buttonBox,2,1)

        ## set widget size
        self.setFixedSize(500,100)

        self.readSettings()


    def selectGSLocation(self):
        gsLocation = QtWidgets.QFileDialog.getOpenFileName(self, "Browse for ghostscript", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.HomeLocation), "*.exe")
        self.txt_gsLocation.setText(gsLocation[0])


    def writeSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")
        settings.setValue("gsLocation", self.txt_gsLocation.text())
        settings.setValue("shouldShowConfigAtLaunch", self.chk_shouldShowConfigAtLaunch.isChecked())
        settings.sync()


    def readSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")
        shouldShowConfigAtLaunch = settings.value("shouldShowConfigAtLaunch")
        if shouldShowConfigAtLaunch == 'true':
            self.chk_shouldShowConfigAtLaunch.setChecked(True)
        elif shouldShowConfigAtLaunch == 'false':
            self.chk_shouldShowConfigAtLaunch.setChecked(False)
        
        gslocation = settings.value("gslocation")
        if gslocation:
            self.txt_gsLocation.setText(gslocation)


    def accept(self):
        self.writeSettings()
        return super().accept()

    # this is called when the application is closed
    def closeEvent(self, event):
        event.accept()