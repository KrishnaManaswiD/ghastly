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
        
        # - file menu
        self.file_menu = QtWidgets.QMenu("File")
        self.menuBar.addMenu(self.file_menu)

        exit_action = QtGui.QAction("Exit", self)
        exit_action.triggered.connect(self.closeApplication)
        self.file_menu.addAction(exit_action)

        # - help menu
        self.help_action = self.menuBar.addAction("Help")
        self.help_action.triggered.connect(self.displayHelp)

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
        self.gridLayout.addWidget(self.btn_moveDown, 4, 2)
        self.gridLayout.addWidget(self.btn_gsLocation, 5, 0)
        self.gridLayout.addWidget(self.txt_gsLocation, 5, 1)
        self.gridLayout.addWidget(self.btn_saveAs, 6, 0)
        self.gridLayout.addWidget(self.txt_saveLocation, 6, 1)
        self.gridLayout.addWidget(self.btn_combine, 6, 2)
        self.mainLayout.addLayout(self.gridLayout)

        self.mainLayout.addWidget(self.statusBar)

        ## Keyboard Shortcuts
        self.shortcut_open = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.openFile)

        self.shortcut_closeApp = QtGui.QShortcut(QtGui.QKeySequence('Alt+F4'), self)
        self.shortcut_closeApp.activated.connect(self.closeApplication)

        self.shortcut_help = QtGui.QShortcut(QtGui.QKeySequence('F1'), self)
        self.shortcut_help.activated.connect(self.displayHelp)

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


    def closeApplication(self):
        sys.exit()  # is this the correct way to do it?

    
    def displayHelp(self):
        helpMessageBox = QtWidgets.QMessageBox()
        helpMessageBox.setWindowTitle("Help")
        helpMessageBox.setWindowIcon(QtGui.QIcon('icon.png'))
        
        helpMessageBox.setText("Steps to use this software")
        helpMessageBox.setTextFormat(QtCore.Qt.RichText)
        helpMessageBox.setInformativeText("Step 1: Download and install ghostscript (3rd party software)\n"+
        "   Visit https://www.ghostscript.com/download/gsdnld.html \n" +
        "   Download the version suited to your operating system \n" +
        "   Install it to an accessible location \n\n" +
        "Step 2: Set the path to the executable by clicking on the GS location button \n" +
        "   On Windows, the executable may be located in the bin folder in the installed location - gswin64.exe \n\n" +
        "Step 3: Choose the pdf files that you want to combine by clicking the Add Files button \n" +
        "   You can add multiple files at once \n" +
        "   You can change the order by clicking on a file in the list and using the Move Up or Move Down buttons \n" +
        "   You can remove a file by selecting it from the list and clicking on the Remove button \n\n" +
        "Step 4: Choose a location to save the combined file \n" +
        "   Click on the Save as button choose a file name and location for the combined output file \n\n" +
        "Step 5: Combine the files \n" +
        "   Click on the Combine button when ready")
        helpMessageBox.setStyleSheet("QLabel{min-width: 600px;}")  # hacky way to set size
        helpMessageBox.exec_()

        #QtWidgets.QMessageBox.information(self, "Help",
        #    "The <b>Application</b> example demonstrates how to "
        #       "write modern GUI applications using Qt, with a menu bar, "
        #       "toolbars, and a status bar.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())