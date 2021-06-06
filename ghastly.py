from settingsDialog import settingsDialog
import sys
import subprocess
from PySide6 import QtCore, QtWidgets, QtGui

class GhastlyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        ## window settings
        self.setWindowTitle("Ghastly")
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        self.setAcceptDrops(True)  # allows dragging and dropping files into the application

        ## variables
        self.shouldShowConfigAtLaunch = False
        self.gsLocation = ""

        ## create widgets
        # tool bar - our application does not have a menu bar
        toolBar = QtWidgets.QToolBar()
        toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        config_action = QtGui.QAction("Config", self)
        config_action.triggered.connect(self.showConfigDialog)
        config_action.setIcon(QtGui.QIcon('icons/icon_config.png'))
        config_action.setIconText("Config")
        toolBar.addAction(config_action)

        help_action = QtGui.QAction("Help", self)
        help_action.triggered.connect(self.showHelpDialog)
        help_action.setIcon(QtGui.QIcon('icons/icon_help.png'))
        help_action.setIconText("Help")
        toolBar.addAction(help_action)

        about_action = QtGui.QAction("About", self)
        about_action.triggered.connect(self.showAboutDialog)
        about_action.setIcon(QtGui.QIcon('icons/icon_about.png'))
        about_action.setIconText("About")
        toolBar.addAction(about_action)

        # labels
        lbl_combineFilesPrompt = QtWidgets.QLabel("Choose files to combine")
        
        # list that showes files
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)  # allows rearanging list by dragging items

        # buttons
        btn_moveUp = QtWidgets.QPushButton("Move Up")
        btn_moveDown = QtWidgets.QPushButton("Move Down")
        btn_add = QtWidgets.QPushButton("Add Files")
        btn_remove = QtWidgets.QPushButton("Remove")
        btn_saveAs = QtWidgets.QPushButton("Save as")
        btn_combine = QtWidgets.QPushButton("Combine")
        #btn_gsLocation = QtWidgets.QPushButton("GS location")
        
        # editable texts
        #txt_gsLocation = QtWidgets.QLineEdit("")
        self.txt_saveLocation = QtWidgets.QLineEdit("")

        # status bar
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.showMessage("Ready")
        self.statusBar.setSizeGripEnabled(False)
        
        ## add key bindings to buttons
        btn_add.clicked.connect(self.openFile)
        btn_saveAs.clicked.connect(self.selectSaveLocation)
        btn_remove.clicked.connect(self.removeItem)
        btn_moveUp.clicked.connect(self.moveItemUp)
        btn_moveDown.clicked.connect(self.moveItemDown)
        #btn_gsLocation.clicked.connect(self.selectGSLocation)
        btn_combine.clicked.connect(self.combineFiles)

        ## create layout and add widgets
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(toolBar)

        # a grid layout that is nested within the main layout
        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(lbl_combineFilesPrompt, 0, 0)
        gridLayout.addWidget(self.listWidget, 1, 0, 4, 2)
        gridLayout.addWidget(btn_add, 1, 2)
        gridLayout.addWidget(btn_remove, 2, 2)
        gridLayout.addWidget(btn_moveUp, 3, 2)
        gridLayout.addWidget(btn_moveDown, 4, 2)
        #gridLayout.addWidget(btn_gsLocation, 5, 0)
        #gridLayout.addWidget(txt_gsLocation, 5, 1)
        gridLayout.addWidget(btn_saveAs, 6, 0)
        gridLayout.addWidget(self.txt_saveLocation, 6, 1)
        gridLayout.addWidget(btn_combine, 6, 2)
        mainLayout.addLayout(gridLayout)

        mainLayout.addWidget(self.statusBar)

        ## Keyboard Shortcuts
        self.shortcut_open = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.openFile)

        self.shortcut_closeApp = QtGui.QShortcut(QtGui.QKeySequence('Alt+F4'), self)
        self.shortcut_closeApp.activated.connect(self.closeEvent)

        self.shortcut_help = QtGui.QShortcut(QtGui.QKeySequence('F1'), self)
        self.shortcut_help.activated.connect(self.showHelpDialog)

        ## set widget size
        self.setFixedSize(700,300)

        ## read settings from saved location
        self.readSettings()
        if self.shouldShowConfigAtLaunch == 'true':
            self.showConfigDialog()

        #if self.gsLocation:
        #    txt_gsLocation.setText(self.gsLocation)        
        

    def openFile(self):
        files, filtr = QtWidgets.QFileDialog.getOpenFileNames(self, "Open Files", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation), "*.pdf")
        self.listWidget.addItems(files)


    def selectSaveLocation(self):
        saveFileLocation = QtWidgets.QFileDialog.getSaveFileName(self, "Save As", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.DocumentsLocation), "*.pdf")
        self.txt_saveLocation.setText(saveFileLocation[0])


    def selectGSLocation(self):
        gsLocation = QtWidgets.QFileDialog.getOpenFileName(self, "Browse for ghostscript", QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.HomeLocation), "*.exe")
        self.txt_gsLocation.setText(gsLocation[0])
        # C:/Program Files/gs/gs9.53.3/bin/


    def moveItemUp(self):
        current = self.listWidget.currentItem()
        currentSelectedIndex = self.listWidget.row(current)
        if currentSelectedIndex > 0:
            self.listWidget.insertItem(currentSelectedIndex-1, self.listWidget.takeItem(currentSelectedIndex))
            self.listWidget.setCurrentRow(currentSelectedIndex-1)


    def moveItemDown(self):
        current = self.listWidget.currentItem()
        currentSelectedIndex = self.listWidget.row(current)
        if currentSelectedIndex < self.listWidget.count():
            self.listWidget.insertItem(currentSelectedIndex+1, self.listWidget.takeItem(currentSelectedIndex))
            self.listWidget.setCurrentRow(currentSelectedIndex+1)
            if self.listWidget.currentRow() == - 1:  # if item has moved to the end, incrementing index makes it -1. revert it to count-1
                self.listWidget.setCurrentRow(self.listWidget.count() - 1)                 

    
    def removeItem(self):
        current = self.listWidget.currentItem()
        self.listWidget.takeItem(self.listWidget.row(current))


    def combineFiles(self):
        self.statusBar.showMessage("Combining files")
        self.readSettings()
        if sys.platform == "win32":
            gsExecutable = self.gsLocation
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
        for index in range(self.listWidget.count()):
            filesToCombine += ' "' + self.listWidget.item(index).text() + '"'

        command = gsExecutable + " " + basicArgs + " " + outputFile + " " + filesToCombine
        subprocess.run(command)
        self.statusBar.showMessage("Output has been saved to " + self.txt_saveLocation.text())

    
    def showHelpDialog(self):
        helpMessageBox = QtWidgets.QMessageBox()
        helpMessageBox.setWindowTitle("Help")
        helpMessageBox.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        
        helpMessageBox.setText("Steps to use this software")
        helpMessageBox.setTextFormat(QtCore.Qt.MarkdownText)
        helpMessageBox.setText("## Steps to using this software  \n" +
        "### Step 1: Download and install ghostscript (3rd party software)  \n" +
        "Visit https://www.ghostscript.com/download/gsdnld.html  \n" +
        "Download the version suited to your operating system  \n" +
        "Install it to an accessible location  \n" +
        "### Step 2: Set the path to the ghostscript executable  \n" +
        "Click on the **Config** button and set the path to the ghostscript ececutable  \n" +
        "On Windows, the executable may be located in the bin folder in the installed location - gswin64.exe  \n" +
        "### Step 3: Choose the pdf files that you want to combine  \n" +
        "Click the **Add Files** button to choose files  \n" +
        "You can add multiple files at once  \n" +
        "You can change the order by clicking on a file in the list and using the **Move Up** or **Move Down** buttons  \n" +
        "You can remove a file by selecting it from the list and clicking on the **Remove** button  \n" +
        "### Step 4: Choose a location to save the combined file  \n" +
        "Click on the **Save as** button choose a file name and location for the combined output file  \n" +
        "### Step 5: Combine the files  \n" +
        "Click on the **Combine** button when ready ")
        helpMessageBox.setStyleSheet("QLabel{min-width: 600px;}")  # hacky way to set size
        helpMessageBox.exec_()


    def showAboutDialog(self):
        aboutMessageBox = QtWidgets.QMessageBox()
        aboutMessageBox.setWindowTitle("About Ghastly")
        aboutMessageBox.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        aboutMessageBox.setTextFormat(QtCore.Qt.MarkdownText)

        aboutMessageBox.setText("## Ghastly is a software to manipulate pdf files.  \n" +
        "You are using version 1.1  \n" +
        "Copyright 2021 Sundara Tejaswi Digumarti and Krishna Manaswi Digumarti. All rights reserved.\n")

        aboutMessageBox.setStyleSheet("QLabel{min-width: 600px;}")  # hacky way to set size
        aboutMessageBox.exec_()


    def showConfigDialog(self):
        configDialog = settingsDialog(self)
        configDialog.exec_()
        pass


    def writeSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")
        settings.sync()


    def readSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")
        self.shouldShowConfigAtLaunch = settings.value("shouldShowConfigAtLaunch")
        self.gsLocation = settings.value("gslocation")


    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        #if event.mimeData().hasFormat("application/pdf"):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event: QtGui.QDragMoveEvent):
        #if event.mimeData().hasFormat("application/pdf"):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event: QtGui.QDropEvent):
        #if event.mimeData().hasFormat("application/pdf"):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

        for url in event.mimeData().urls():
            if url.isLocalFile():
                # check if file is pdf
                fileName = url.toLocalFile()
                suffix = QtCore.QFileInfo(fileName).suffix()
                if suffix == "pdf":
                    self.listWidget.addItem(fileName)
        

    # this is called when the application is closed
    def closeEvent(self, event):
        self.writeSettings()
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    ghastly = GhastlyWidget()
    ghastly.show()

    sys.exit(app.exec_())