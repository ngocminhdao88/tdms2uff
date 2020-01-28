# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from view import Ui_Dialog
from tdms_obj_list_model import TdmsObjListModel, TdmsObj
from treeitem import TreeItem
from treemodel import TreeModel

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self.outputDir = ""

        headers = ["Name", "Description"]
        data = "Getting Started     How to familiarize yourself with Qt Designer"

        self.sorceModel = TreeModel(headers, data)
        self.inputProxyModel = QSortFilterProxyModel(self)
        self.inputProxyModel.setSourceModel(self.sourceModel)

        self.outputProxyModel = QSortFilterProxyModel(self)
        self.outputProxyModel.setSourceModel(self.sourceModel)

        self.inputTreeView.setModel(self.inputProxyModel)
        self.outputTreeView.setModel(self.outputProxyModel)

        self.addFilesButton.clicked.connect(self.addFiles)
        self.addFolderButton.clicked.connect(self.addDir)
        self.removeFromInputButton.clicked.connect(self.removeFromInput)
        self.addToOutputQueueButton.clicked.connect(self.addToOutputQueue)

        self.setOutputFolderButton.clicked.connect(self.setOutputDir)
        self.convertButton.clicked.connect(self.runOutputQueue)
        self.removeFromOutputButton.clicked.connect(self.removeFromOutput)
        self.backToInputButton.clicked.connect(self.backToInput)

    @pyqtSlot()
    def removeFromInput(self):
        #Remove input files
        indexes = self.inputListView.selectedIndexes()

        if len(indexes) > 0:
            #Remove obj in reverse so it doesn't mess up the subsequent indexes
            for index in sorted(indexes, reverse=True):
                self.inputModel.removeRow(index.row())

    @pyqtSlot()
    def removeFromOutput(self):
        #Remove output files
        indexes = self.outputListView.selectedIndexes()

        if len(indexes) > 0:
            #Remove obj in reverse so it doesn't mess up the subsequent indexes
            for index in sorted(indexes, reverse=True):
                self.outputListModel.removeRow(index.row())

    @pyqtSlot()
    def addFiles(self):
        #Open a dialog to select one or multiple files
        filePaths = QFileDialog.getOpenFileNames(
                self,
                "Select one or more files",
                ".",
                "TDMS (*.tdms)")

        #extract only the file path
        filePaths = filePaths[0]
        objs = []

        for filePath in filePaths:
            obj = TdmsObj(filePath)
            objs.append(item)

        self.inputModel.addTdmsObjs(objs)

    @pyqtSlot()
    def addDir(self):
        #Open a dialog to select working directory
        selectedDir = QFileDialog.getExistingDirectory(
                self,
                "Open directory",
                ".",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        #Add only tdms files into the input model
        if len(selectedDir) > 0:
            dirObj = QDir(selectedDir)
            entryInfoList = dirObj.entryInfoList(
                    ["*.tdms"],
                    QDir.Files)

            objs = []

            for fileInfo in entryInfoList:
                tdmsObj = TdmsObj(fileInfo.absoluteFilePath())
                objs.append(tdmsObj)

            self.inputModel.addTdmsObjs(objs)

    @pyqtSlot()
    def setOutputDir(self):
        #Ask user to select the output folder
        selectedDir = QFileDialog.getExistingDirectory(
                self,
                "Set output directory",
                ".",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        if selectedDir != self.outputDir:
            self.outputDir = selectedDir

    @pyqtSlot()
    def addToOutputQueue(self):
        #Add selected files into working queue
        indexes = self.inputListView.selectedIndexes()

        if len(indexes) > 0:
            tdmsObjs = []
            for index in sorted(indexes, reverse=True):
                tdmsObj = self.inputModel.data(index, role=TdmsObjListModel.ObjRole)
                self.inputModel.removeRow(index.row())
                tdmsObjs.append(tdmsObj)

            self.outputListModel.addTdmsObjs(tdmsObjs)

    @pyqtSlot()
    def backToInput(self):
        #Add selected files into working queue
        indexes = self.outputListView.selectedIndexes()

        if len(indexes) > 0:
            tdmsObjs = []
            for index in sorted(indexes, reverse=True):
                tdmsObj = self.outputListModel.data(index, role=TdmsObjListModel.ObjRole)
                self.outputListModel.removeRow(index.row())
                tdmsObjs.append(tdmsObj)

            self.inputModel.addTdmsObjs(tdmsObjs)


    @pyqtSlot()
    def runOutputQueue(self):
        #Convert the files in working queue
        pass
