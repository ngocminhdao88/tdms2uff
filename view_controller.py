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
from counter import Counter

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self._setupStatusMachine()

        self.outputDir = ""


        #self._outputStatusMachine = QStateMachine()

        self._threadPool = QThreadPool() #manage worker objects

        headers = ["Name", "Type", "Unit", "Description"]
        data = []

        #MODELS
        self.sourceModel = TreeModel(headers, data)

        self.inputProxyModel = QSortFilterProxyModel(self)
        self.inputProxyModel.setSourceModel(self.sourceModel)

        self.outputModel = TreeModel(headers, data)

        #VIEWS
        self.inputListView.setModel(self.inputProxyModel)

        self.channelsTreeView.setModel(self.sourceModel)

        self.outputListView.setModel(self.outputModel)

        #SIGNALS->SLOTS
        self.inputListView.clicked.connect(self.updateChannelsTreeView)
        self.inputFilterEdit.textChanged.connect(self.inputProxyModel.setFilterRegExp)
        self.addFilesButton.clicked.connect(self.addFiles)
        self.addFolderButton.clicked.connect(self.addDir)
        self.removeFromInputButton.clicked.connect(self.removeFromInput)
        self.addToOutputButton.clicked.connect(self.addToOutputQueue)

        self.setOutputFolderButton.clicked.connect(self.setOutputDir)
        self.convertButton.clicked.connect(self.runOutputQueue)
        self.removeFromOutputButton.clicked.connect(self.removeFromOutput)
        self.backToInputButton.clicked.connect(self.backToInput)


    def _setupStatusMachine(self):
        """
        Setup the state machine to update the workstatus
        of import tdms files and converting tdms files to uff files
        """
        #setup a state machine to update the import file status
        self._importCounter = Counter()
        self._importStatusMachine = QStateMachine()

        self._importIdleState = QState()
        self._importIdleState.assignProperty(self.inputStatus, "text", "<b>idle</b>")

        self._importWorkingState = QState()
        self._importWorkingState.assignProperty(self.inputStatus, "text", "<b>importing...</b>")

        self._import_idleToWorkingTrans = QSignalTransition(self._importCounter.started)
        self._import_idleToWorkingTrans.setTargetState(self._importWorkingState)
        self._import_workingToIdleTrans = QSignalTransition(self._importCounter.tripped)
        self._import_workingToIdleTrans.setTargetState(self._importIdleState)

        self._importIdleState.addTransition(self._import_idleToWorkingTrans)
        self._importWorkingState.addTransition(self._import_workingToIdleTrans)

        self._importStatusMachine.addState(self._importIdleState)
        self._importStatusMachine.addState(self._importWorkingState)
        self._importStatusMachine.setInitialState(self._importIdleState)

        self._importStatusMachine.start()

        #setup a state machine to update the converting work status
        self._outputCounter = Counter()
        self._outputStatusMachine = QStateMachine()

        self._outputIdleState = QState()
        self._outputIdleState.assignProperty(self.outputStatus, "text", "<b>idle</b>")

        self._outputWorkingState = QState()
        self._outputWorkingState.assignProperty(self.outputStatus, "text", "<b>converting...</b>")

        self._output_idleToWorkingTrans = QSignalTransition(self._outputCounter.started)
        self._output_idleToWorkingTrans.setTargetState(self._outputWorkingState)
        self._output_workingToIdleTrans = QSignalTransition(self._outputCounter.tripped)
        self._output_workingToIdleTrans.setTargetState(self._outputIdleState)

        self._outputIdleState.addTransition(self._output_idleToWorkingTrans)
        self._outputWorkingState.addTransition(self._output_workingToIdleTrans)

        self._outputStatusMachine.addState(self._outputIdleState)
        self._outputStatusMachine.addState(self._outputWorkingState)
        self._outputStatusMachine.setInitialState(self._outputIdleState)

        self._outputStatusMachine.start()


    @pyqtSlot(QModelIndex)
    def updateChannelsTreeView(self, index):
        #Show all channels of selected input file
        if not index.isValid():
            return

        #get the index in source model from the proxy index
        #and then set the root index of channel view to it
        proxyModel = index.model() #proxymodel
        sourceModel = proxyModel.sourceModel()
        sourceIndex = proxyModel.mapToSource(index)
        self.channelsTreeView.setRootIndex(sourceIndex)

        #fit the column width in channel view to its contents
        for i in range(self.sourceModel.columnCount()):
            self.channelsTreeView.resizeColumnToContents(i)


    @pyqtSlot()
    def removeFromInput(self):
        """
        Remove selected items from input list view
        :return: None
        """
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

        rootItem = self.sourceModel.rootItem()

        self.sourceModel.layoutAboutToBeChanged.emit()
        rootItem.addChild(obj)
        self.sourceModel.layoutChanged.emit()


    @pyqtSlot()
    def removeFromOutput(self):
        """
        Remove selected items from output list view
        :return: None
        """
        indexes = self.outputListView.selectedIndexes()

        if len(indexes) > 0:
            #Remove obj in reverse so it doesn't mess up the subsequent indexes
            for index in sorted(indexes, reverse=True):
                self.outputModel.removeRow(index.row(), index.parent())


    @pyqtSlot()
    def addFiles(self):
        """
        Open a dialog to select one or multiple files
        :return: None
        """
        filePaths = QFileDialog.getOpenFileNames(
                self,
                "Select one or more files",
                ".",
                "TDMS (*.tdms)")

        #extract only the file path
        filePaths = filePaths[0]
        if len(filePaths) > 0:
            converter = TdmsTreeItemConverter()
            self._addFiles(filePaths)


    @pyqtSlot()
    def addDir(self):
        """
        Import multiple files from a folder
        """
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

            filePaths = []
            for fileInfo in entryInfoList:
                filePath = fileInfo.absoluteFilePath()
                filePaths.append(filePath)

            self._addFiles(filePaths)


    def _addFiles(self, filePaths):
        """
        Add multiple files into input model
        :param filePaths: [str]
        :return: None
        """
        self._importCounter.reset()
        self._importCounter.setPreset(len(filePaths))
        self._importCounter.started.emit()

        for filePath in filePaths:
            worker = TdmsImportWorker(filePath)

            worker.signals.result.connect(self.updateSourceModel)
            worker.signals.finished.connect(self._importCounter.countUp)

            self._threadPool.start(worker)



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
        """
        Add selected files into working queue (output model)
        :return: None
        """
        leftSelection = self.inputListView.selectedIndexes()
        proxyModel = self.inputListView.model()
        sourceModel = proxyModel.sourceModel()
        columnCount = sourceModel.columnCount()
        rightModel = self.outputModel
        rightModelRootItem = rightModel.rootItem()

        converter = TdmsTreeItemConverter()

        if not len(leftSelection) > 0:
            return

        rightModel.layoutAboutToBeChanged.emit()

        #add selected item to output view
        for idx in leftSelection:
            #copy a new treeitem by converting it a neutral tdmsobj first
            #and then create a new treeitem from it
            sourceIdx = proxyModel.mapToSource(idx)
            item = sourceModel.getItem(sourceIdx)
            tdmsObj = converter.toTdmsObj(item)
            newItem = converter.toTreeItem(tdmsObj, columnCount)
            rightModelRootItem.addChild(newItem)

        rightModel.layoutChanged.emit()

        #remove selected item from input view
        for idx in sorted(leftSelection, reverse=True):
            sourceIdx = proxyModel.mapToSource(idx)
            sourceModel.removeRow(sourceIdx.row(), sourceIdx.parent())



    @pyqtSlot()
    def backToInput(self):
        """
        Move selected files back into input view (source model). Right -> Left
        :return: None
        """
        rightSelection = self.outputListView.selectedIndexes()
        rightModel = self.outputListView.model()
        leftModel = self.sourceModel
        leftModelRootItem = leftModel.rootItem()

        columnCount = rightModel.columnCount()

        converter = TdmsTreeItemConverter()

        if not len(rightSelection) > 0:
            return

        leftModel.layoutAboutToBeChanged.emit()

        #add selected item back to input view
        for idx in rightSelection:
            #copy a new treeitem by converting it a neutral tdmsobj first
            #and then create a new treeitem from it
            item = rightModel.getItem(idx)
            tdmsObj = converter.toTdmsObj(item)
            newItem = converter.toTreeItem(tdmsObj, columnCount)
            leftModelRootItem.addChild(newItem)

        leftModel.layoutChanged.emit()

        #remove selected item from output view
        for idx in sorted(rightSelection, reverse=True):
            rightModel.removeRow(idx.row(), idx.parent())


    @pyqtSlot()
    def runOutputQueue(self):
        #Convert the files in working queue to UFF
        #by sending it to the TdmsUffWorker
        indexes = self.outputListView.selectedIndexes()

        if len(indexes) > 0:
            tdmsObjs = []

            converter = TdmsTreeItemConverter()

            sourceModel = self.outputListView.model()
            columnCount = sourceModel.columnCount()

            for idx in indexes:
                dataSetItem = sourceModel.getItem(idx)
                tdmsObj = converter.toTdmsObj(dataSetItem)

                tdmsObjs.append(tdmsObj)

            self._outputCounter.reset()
            self._outputCounter.setPreset(len(tdmsObjs))
            self._outputCounter.started.emit()

            for obj in tdmsObjs:
                worker = TdmsUffWorker(obj, self.outputDir)

                worker.signals.finished.connect(self._outputCounter.countUp)

                self._threadPool.start(worker)
