# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from view import Ui_Dialog
from tdms_item import TdmsItem
from tdms_list_model import TdmsListModel

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self.tdmsListModel = TdmsListModel()
        self.inputFilesListView.setModel(self.tdmsListModel)

        self.openFilesButton.clicked.connect(self.openFiles)
        self.openFolderButton.clicked.connect(self.openDir)
        self.removeButton.clicked.connect(self.remove)

    @pyqtSlot()
    def remove(self):
        #Remove input files
        indexes = self.inputFilesListView.selectedIndexes()

        if len(indexes) > 0:
            index = indexes[0]
            #Remove the item from model
            self.tdmsListModel.removeRows(index.row(), 1)

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
        items = []

        for filePath in filePaths:
            item = TdmsItem(filePath)
            items.append(item)

        self.tdmsListModel.addItems(items)

    @pyqtSlot()
    def openDir(self):
        #Open a dialog to select working directory
        dirPath = QFileDialog.getExistingDirectory(
                self,
                "Open directory",
                ".",
                QFileDialog.ShowDirsOnly | QFileDialog.DontConfirmOverwrite)

        #print(dirPath)

    @pyqtSlot()
    def addToQueue(self):
        #Add selected files into working queue
        pass

    @pyqtSlot()
    def convert(self):
        #Convert the files in working queue
        pass

