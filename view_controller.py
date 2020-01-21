# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from view import Ui_Dialog

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self.openFilesButton.clicked.connect(self.openFiles)
        self.openFolderButton.clicked.connect(self.openDir)

    @pyqtSlot()
    def openFiles(self):
        #Open a dialog to select one or multiple files
        filePaths = QFileDialog.getOpenFileNames(
                self,
                "Select one or more files",
                ".",
                "TDMS (*.tdms)")

        #extract only the file path
        filePaths = filePaths[0]
        print(filePaths)

    @pyqtSlot()
    def openDir(self):
        #Open a dialog to select working directory
        dirPath = QFileDialog.getExistingDirectory(
                self,
                "Open directory",
                ".",
                QFileDialog.ShowDirsOnly | QFileDialog.DontConfirmOverwrite)

        print(dirPath)

    @pyqtSlot()
    def addToQueue(self):
        #Add selected files into working queue
        pass

    @pyqtSlot()
    def convert(self):
        #Convert the files in working queue
        pass
