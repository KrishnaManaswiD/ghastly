import sys
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        ## some variables
        self.listOfFilesToCombine = []

        ## window settings
        self.setWindowTitle("Ghastly")
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        ## create widgets
        # menu bar
        self.menuBar = QtWidgets.QMenuBar()
        self.file_menu = self.menuBar.addMenu("File")
        self.file_menu = self.menuBar.addMenu("Help")

        # labels
        self.lbl_combineFilesPrompt = QtWidgets.QLabel("Choose files to combine")
        
        # list that displayes files
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        # buttons
        self.btn_moveUp = QtWidgets.QPushButton("Move Up")
        self.btn_moveDown = QtWidgets.QPushButton("Move Down")
        self.btn_add = QtWidgets.QPushButton("Add Files")
        self.btn_remove = QtWidgets.QPushButton("Remove")
        self.btn_saveAs = QtWidgets.QPushButton("Save as")
        self.btn_combine = QtWidgets.QPushButton("Combine")
        self.btn_gsLocation = QtWidgets.QPushButton("GS location")
        
        # editable texts
        self.txt_gsLocation = QtWidgets.QLineEdit("")
        self.txt_saveLocation = QtWidgets.QLineEdit("")

        # status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.showMessage("Ready")
        self.statusBar.setSizeGripEnabled(False)
        
        ## add key bindings to buttons
        self.btn_add.clicked.connect(self.openFile)
        self.btn_saveAs.clicked.connect(self.selectSaveLocation)
        self.btn_remove.clicked.connect(self.removeItem)
        self.btn_moveUp.clicked.connect(self.moveItemUp)
        self.btn_moveDown.clicked.connect(self.moveItemDown)
        self.btn_gsLocation.clicked.connect(self.selectGSLocation)
        self.btn_combine.clicked.connect(self.combineFiles)

        ## create layout and add widgets
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.addWidget(self.menuBar)

        # a grid layout that is nested within the main layout
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.addWidget(self.lbl_combineFilesPrompt, 0, 0)
        self.gridLayout.addWidget(self.listWidget, 1, 0, 4, 2)
        self.gridLayout.addWidget(self.btn_add, 1, 2)
        self.gridLayout.addWidget(self.btn_remove, 2, 2)
        self.gridLayout.addWidget(self.btn_moveUp, 3, 2)
        self.gridLayout.addWidget(self.btn_moveDown, 3, 2)
        self.gridLayout.addWidget(self.btn_gsLocation, 5, 0)
        self.gridLayout.addWidget(self.txt_gsLocation, 5, 1)
        self.gridLayout.addWidget(self.btn_saveAs, 6, 0)
        self.gridLayout.addWidget(self.txt_saveLocation, 6, 1)
        self.gridLayout.addWidget(self.btn_combine, 6, 2)
        self.mainLayout.addLayout(self.gridLayout)

        self.mainLayout.addWidget(self.statusBar)

        ## set widget size
        self.setFixedSize(700,300)
        

    def openFile(self):
        files, filtr = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Files", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation), "*.pdf")
        self.listOfFilesToCombine.extend(files)
        self.updateList()


    def selectSaveLocation(self):
        saveFileLocation = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation), "*.pdf")
        self.txt_saveLocation.setText(saveFileLocation[0])


    def selectGSLocation(self):
        gsLocation = QtWidgets.QFileDialog.getOpenFileName(self, "Browse for ghost script", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.HomeLocation), "*.exe")
        self.txt_gsLocation.setText(gsLocation[0])
        # C:/Program Files/gs/gs9.53.3/bin/


    def combineFiles(self):
        self.statusBar.showMessage("Combining files")
        if sys.platform == "win32":
            gsExecutable = self.txt_gsLocation.text()
        elif sys.platform == "linux":
            gsExecutable = "gs"

        # check if gsExecutable is set
        if not gsExecutable:
            self.statusBar.showMessage("Ghostscript location has not been set correctly")
            return

        basicArgs = "-dBATCH -dNOPAUSE -sDEVICE=pdfwrite -dAutoRotatePages=/None -dAutoFilterColorImages=false -dAutoFilterGrayImages=false -dColorImageFilter=/FlateEncode -dGrayImageFilter=/FlateEncode -dDownsampleMonoImages=false -dDownsampleGrayImages=false"
        
        # check if save location has been set
        if not self.txt_saveLocation.text():
            self.statusBar.showMessage("Please check where you want to save the output file")
            return

        outputFile = "-sOutputFile=" + '"' + self.txt_saveLocation.text() +'"'
                
        filesToCombine = ""
        for item in self.listOfFilesToCombine:
            filesToCombine += ' "' + item + '"'

        command = gsExecutable + " " + basicArgs + " " + outputFile + " " + filesToCombine
        subprocess.run(command)
        self.statusBar.showMessage("Output has been saved to " + self.txt_saveLocation.text())


    def moveItemUp(self):
        current = self.listWidget.currentItem()
        currentSelectedIndex = self.listWidget.row(current)
        if currentSelectedIndex > 0:
            self.listOfFilesToCombine.insert(currentSelectedIndex-1, self.listOfFilesToCombine.pop(currentSelectedIndex))
            self.updateList()


    def moveItemDown(self):
        current = self.listWidget.currentItem()
        currentSelectedIndex = self.listWidget.row(current)
        if currentSelectedIndex < len(self.listOfFilesToCombine)-1:
            self.listOfFilesToCombine.insert(currentSelectedIndex+1, self.listOfFilesToCombine.pop(currentSelectedIndex))
            self.updateList()

    
    def removeItem(self):
        current = self.listWidget.currentItem()
        self.listOfFilesToCombine.pop(self.listWidget.row(current))
        self.updateList()


    def updateList(self):
        self.listWidget.clear()
        for item in self.listOfFilesToCombine:
            self.listWidget.addItem(item)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())