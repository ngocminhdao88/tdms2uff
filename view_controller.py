# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from view import Ui_Dialog
from tdmsobj import TdmsObj
from treeitem import TreeItem
from treemodel import TreeModel
from converter import TdmsTreeItemConverter
from worker import TdmsUffWorker, TdmsImportWorker

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self.outputDir = ""

        self._threadPool = QThreadPool() #manage worker objects

        headers = ["Name", "Type", "Unit", "Description"]
        data = []

        self.sourceModel = TreeModel(headers, data)

        self.inputProxyModel = QSortFilterProxyModel(self)
        self.inputProxyModel.setSourceModel(self.sourceModel)

        self.outputProxyModel = QSortFilterProxyModel(self)
        self.outputProxyModel.setSourceModel(self.sourceModel)

        self.inputListView.setModel(self.inputProxyModel)
        self.inputListView.clicked.connect(self.updateChannelsTreeView)

        self.channelsTreeView.setModel(self.inputProxyModel)
        self.outputListView.setModel(self.outputProxyModel)

        self.inputFilterEdit.textChanged.connect(self.inputProxyModel.setFilterRegExp)

        self.addFilesButton.clicked.connect(self.addFiles)
        self.addFolderButton.clicked.connect(self.addDir)
        self.removeFromInputButton.clicked.connect(self.removeFromInput)
        self.addToOutputButton.clicked.connect(self.addToOutputQueue)

        self.setOutputFolderButton.clicked.connect(self.setOutputDir)
        self.convertButton.clicked.connect(self.runOutputQueue)
        self.removeFromOutputButton.clicked.connect(self.removeFromOutput)
        self.backToInputButton.clicked.connect(self.backToInput)

    @pyqtSlot(QModelIndex)
    def updateChannelsTreeView(self, index):
        #Show all channels of selected input file
        if not index.isValid():
            return

        #TODO: not working when input is filterd


        """
        model = index.model() #proxymodel
        sourceModel = model.sourceModel()
        sourceIndex = model.mapToSource(index)

        proxyIndex = model.mapFromSource(sourceIndex)
        self.channelsTreeView.setRootIndex(proxyIndex)
        """

        self.channelsTreeView.setRootIndex(index)


        #fit the column width
        for i in range(self.sourceModel.columnCount()):
            self.channelsTreeView.resizeColumnToContents(i)

    @pyqtSlot()
    def removeFromInput(self):
        #Remove selected items from input list view
        indexes = self.inputListView.selectedIndexes()
        model = self.inputListView.model() #proxymodel
        sourceModel = model.sourceModel()

        if len(indexes) > 0:
            #Remove obj in reverse so it doesn't mess up the subsequent indexes
            for index in sorted(indexes, reverse=True):
                sourceIndex = model.mapToSource(index)
                sourceModel.removeRow(sourceIndex.row(), sourceIndex.parent())

    @pyqtSlot(object)
    def updateSourceModel(self, obj):
        """
        Update the source model
        """
        if not obj:
            return

        proxyModel = self.inputListView.model()
        sourceModel = proxyModel.sourceModel()
        rootItem = sourceModel.rootItem()

        sourceModel.layoutAboutToBeChanged.emit()
        rootItem.addChild(obj)
        sourceModel.layoutChanged.emit()

    @pyqtSlot()
    def removeFromOutput(self):
        #Remove output files
        pass

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
        converter = TdmsTreeItemConverter()

        for filePath in filePaths:
            self._addFile(filePath)

    def _addFile(self, filePath):
        """
        Start a TdmsImportWorker thread to import big tdms file
        """
        worker = TdmsImportWorker(filePath)
        worker.signals.result.connect(self.updateSourceModel)

        self._threadPool.start(worker)

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

            for fileInfo in entryInfoList:
                filePath = fileInfo.absoluteFilePath()
                self._addFile(filePath)

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
        pass

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
        #Convert the files in working queue to UFF
        #by sending it to the TdmsUffWorker
        indexes = self.outputListView.selectedIndexes()

        if len(indexes) > 0:
            tdmsObjs = []
            converter = TdmsTreeItemConverter()

            proxyModel = self.outputListView.model()
            sourceModel = proxyModel.sourceModel()

            for idx in indexes:
                sourceIdx = proxyModel.mapToSource(idx)
                dataSetItem = sourceModel.getItem(sourceIdx)
                tdmsObj = converter.toTdmsObj(dataSetItem, 4)

                tdmsObjs.append(tdmsObj)

            for obj in tdmsObjs:
                worker = TdmsUffWorker(obj, self.outputDir)
                self._threadPool.start(worker)
