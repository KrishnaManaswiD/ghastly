from settingsDialog import settingsDialog
import requests
import webbrowser
import sys
import subprocess
import ctypes
from ctypes.util import find_library
from PySide6 import QtCore, QtWidgets, QtGui
from PyPDF2 import PdfFileMerger

class GhastlyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        ## version check
        version_file = open("version.txt", "r")
        self.local_version = float(version_file.read())
        version_file.close()

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

        #config_action = QtGui.QAction("Config", self)
        #config_action.triggered.connect(self.showConfigDialog)
        #config_action.setIcon(QtGui.QIcon('icons/icon_config.png'))
        #config_action.setIconText("Config")
        #toolBar.addAction(config_action)

        # dummy widget to right align buttons in tool bar
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        toolBar.addWidget(spacer)

        help_btn_action = QtGui.QAction("Help", self)
        help_btn_action.triggered.connect(self.showHelpDialog)
        help_btn_action.setIcon(QtGui.QIcon('icons/icon_help.png'))
        help_btn_action.setIconText("Help")
        toolBar.addAction(help_btn_action)

        about_btn_action = QtGui.QAction("About", self)
        about_btn_action.triggered.connect(self.showAboutDialog)
        about_btn_action.setIcon(QtGui.QIcon('icons/icon_about_dark.png'))
        about_btn_action.setIconText("About")
        toolBar.addAction(about_btn_action)

        donate_btn_action = QtGui.QAction("Donate", self)
        donate_btn_action.triggered.connect(self.showAboutDialog)
        donate_btn_action.setIcon(QtGui.QIcon('icons/icon_donate.png'))
        donate_btn_action.setIconText("Donate")
        toolBar.addAction(donate_btn_action)

        ## thse go into the first tab
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
        btn_combine.clicked.connect(self.combineFiles2)

        ## create layout and add widgets
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.addWidget(toolBar)

        # various features are grouped into tabs. eg. conbine files, config etc.
        tabWidget = QtWidgets.QTabWidget()
        mainLayout.addWidget(tabWidget)

        # a grid layout that is nested within the first tab of the tab wiget
        gridLayoutForTab1 = QtWidgets.QGridLayout()
        gridLayoutForTab1.addWidget(lbl_combineFilesPrompt, 0, 0)
        gridLayoutForTab1.addWidget(self.listWidget, 1, 0, 4, 2)
        gridLayoutForTab1.addWidget(btn_add, 1, 2)
        gridLayoutForTab1.addWidget(btn_remove, 2, 2)
        gridLayoutForTab1.addWidget(btn_moveUp, 3, 2)
        gridLayoutForTab1.addWidget(btn_moveDown, 4, 2)
        #gridLayout.addWidget(btn_gsLocation, 5, 0)
        #gridLayout.addWidget(txt_gsLocation, 5, 1)
        gridLayoutForTab1.addWidget(btn_saveAs, 6, 0)
        gridLayoutForTab1.addWidget(self.txt_saveLocation, 6, 1)
        gridLayoutForTab1.addWidget(btn_combine, 6, 2)
        #mainLayout.addLayout(gridLayout)

        tab1 = QtWidgets.QWidget()
        tab1.setLayout(gridLayoutForTab1)
        tabWidget.addTab(tab1,"Basic")

        # a grid layout that is nested within the second tab of the tab wiget
        gridLayoutForTab2 = QtWidgets.QGridLayout()
        
        tab2 = QtWidgets.QWidget()
        tab2.setLayout(gridLayoutForTab2)
        tabWidget.addTab(tab2,"Config")

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
        
        # check if ghostscript is installed and set on path
        gsExecutable = ""
        if sys.platform == "win32":
            gsdll = find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll")))
            if gsdll == "":
                self.statusBar.showMessage("Ghostscript location has not been set correctly")
                return
            else:
                if gsdll[-5] == "4": # if gsdll is gsdll64.dll, set executable to gswin64c.exe
                    gsExecutable = "gswin64c.exe"
                if gsdll[-5] == "2": # if gsdll is gsdll32.dll, set executable to gswin32c.exe
                    gsExecutable = "gswin32c.exe"
        elif sys.platform == "linux" or sys.platform == "darwin":
            gsLibrary = find_library("gs")
            if gsdll == "":
                self.statusBar.showMessage("Ghostscript location has not been set correctly")
                return
            else:
                gsExecutable = "gs"           

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

    
    def combineFiles2(self):
        self.statusBar.showMessage("Combining files")
               
        # check if save location has been set
        if not self.txt_saveLocation.text():
            self.statusBar.showMessage("Please check where you want to save the output file")
            return

        outputFile = self.txt_saveLocation.text()
                
        filesToCombine = []
        merger = PdfFileMerger()
        for index in range(self.listWidget.count()):
            merger.append(self.listWidget.item(index).text())

        merger.write(outputFile)
        merger.close()
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

        # todo: add a check for what happens when internet fails
        isUpdateAvailable, latest_version = self.checkForUpdate()

        aboutMessageBox.setText("## Ghastly is a software to manipulate pdf files.  \n" +
        "You are using version " + str(self.local_version) + "  \n" +
        "Latest released version is " + str(latest_version) + "  \n" +
        "Copyright 2021 Sundara Tejaswi Digumarti and Krishna Manaswi Digumarti.\n")

        btn_update = QtWidgets.QPushButton("Update")
        btn_update.clicked.connect(self.updateSoftware)

        aboutMessageBox.addButton(QtWidgets.QMessageBox.Ok)

        if(isUpdateAvailable):
            aboutMessageBox.addButton(btn_update, QtWidgets.QMessageBox.ActionRole)
        
        aboutMessageBox.setStyleSheet("QLabel{min-width: 600px;}")  # hacky way to set size
        aboutMessageBox.exec_()


    def showConfigDialog(self):
        configDialog = settingsDialog(self)
        configDialog.exec_()
        pass


    def checkForUpdate(self):
        latest_version_request = requests.get("https://raw.githubusercontent.com/KrishnaManaswiD/ghastly/main/version.txt")
        if latest_version_request.status_code == 200:
            latest_version = float(latest_version_request.text)
            if (self.local_version < latest_version):
                return True, latest_version
            else:
                return False, self.local_version
        return False, self.local_version


    def updateSoftware(self):
        webbrowser.open("https://github.com/KrishnaManaswiD/ghastly/releases")


    def writeSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")
        settings.sync()


    def readSettings(self):
        settings = QtCore.QSettings("TandM", "Ghastly")


    def isGhostscriptInstalled(self):
        if find_library("".join(("gsdll", str(ctypes.sizeof(ctypes.c_voidp) * 8), ".dll"))) != "":
            return True
        else:
            return False


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