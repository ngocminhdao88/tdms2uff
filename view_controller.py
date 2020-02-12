# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from view import Ui_Dialog
from tdmsobj import TdmsObj
from treeitem import TreeItem
from treemodel import TreeModel
from converter import TdmsTreeItemConverter
from worker import *
from counter import Counter
from my_statemachine import *

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self._setupStatusMachine()

        self.outputDir = ""

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
        self.inputListView.setAlternatingRowColors(True)

        self.channelsTreeView.setModel(self.sourceModel)
        self.channelsTreeView.setAlternatingRowColors(True)

        self.outputListView.setModel(self.outputModel)
        self.outputListView.setAlternatingRowColors(True)

        #SIGNALS->SLOTS
        self.inputListView.clicked.connect(self.updateChannelsTreeView)
        self.inputFilterEdit.textChanged.connect(self.inputProxyModel.setFilterRegExp)
        self.addFilesButton.clicked.connect(self.addFiles)
        self.addFolderButton.clicked.connect(self.addFolder)
        self.addSubfolderButton.clicked.connect(self.addSubfolder)
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
        self._importIdleState.assignProperty(self.inputStateLabel, "text", "idle")
        self._importIdleState.assignProperty(self.inputProgressLabel, "visible", False)
        self._importIdleState.assignProperty(self.addFilesButton, "enabled", True)
        self._importIdleState.assignProperty(self.addFolderButton, "enabled", True)
        self._importIdleState.assignProperty(self.addSubfolderButton, "enabled", True)
        self._importIdleState.assignProperty(self.removeFromInputButton, "enabled", True)
        self._importIdleState.assignProperty(self.addToOutputButton, "enabled", True)

        self._importSearchingState = QState()
        self._importSearchingState.assignProperty(self.inputStateLabel, "text", "searching..")
        self._importSearchingState.assignProperty(self.addSubfolderButton, "enabled", False)

        self._importWorkingState = QState()
        self._importWorkingState.assignProperty(self.inputStateLabel, "text", "importing... ")
        self._importWorkingState.assignProperty(self.inputProgressLabel, "visible", True)
        self._importWorkingState.assignProperty(self.addFilesButton, "enabled", False)
        self._importWorkingState.assignProperty(self.addFolderButton, "enabled", False)
        self._importWorkingState.assignProperty(self.addSubfolderButton, "enabled", False)
        self._importWorkingState.assignProperty(self.removeFromInputButton, "enabled", False)
        self._importWorkingState.assignProperty(self.addToOutputButton, "enabled", False)

        self._import_idleToWorkingTrans = QSignalTransition(self._importCounter.started)
        self._import_idleToWorkingTrans.setTargetState(self._importWorkingState)
        self._import_workingToIdleTrans = QSignalTransition(self._importCounter.tripped)
        self._import_workingToIdleTrans.setTargetState(self._importIdleState)

        self._import_idleToSearchingTrans = StartSearchingTransition()
        self._import_idleToSearchingTrans.setTargetState(self._importSearchingState)

        self._import_searchingToWorkingTrans = EndSearchingTransition()
        self._import_searchingToWorkingTrans.setTargetState(self._importWorkingState)

        self._importIdleState.addTransition(self._import_idleToWorkingTrans)
        self._importIdleState.addTransition(self._import_idleToSearchingTrans)

        self._importSearchingState.addTransition(self._import_searchingToWorkingTrans)

        self._importWorkingState.addTransition(self._import_workingToIdleTrans)

        self._importStatusMachine.addState(self._importIdleState)
        self._importStatusMachine.addState(self._importSearchingState)
        self._importStatusMachine.addState(self._importWorkingState)

        self._importStatusMachine.setInitialState(self._importIdleState)

        self._importStatusMachine.start()

        #setup a state machine to update the converting work status
        self._outputCounter = Counter()
        self._outputStatusMachine = QStateMachine()

        self._outputIdleState = QState()
        self._outputIdleState.assignProperty(self.outputStateLabel, "text", "idle")
        self._outputIdleState.assignProperty(self.outputProgressLabel, "visible", False)
        self._outputIdleState.assignProperty(self.convertButton, "enabled", True)
        self._outputIdleState.assignProperty(self.removeFromOutputButton, "enabled", True)
        self._outputIdleState.assignProperty(self.backToInputButton, "enabled", True)

        self._outputWorkingState = QState()
        self._outputWorkingState.assignProperty(self.outputStateLabel, "text", "converting... ")
        self._outputWorkingState.assignProperty(self.outputProgressLabel, "visible", True)
        self._outputWorkingState.assignProperty(self.convertButton, "enabled", False)
        self._outputWorkingState.assignProperty(self.removeFromOutputButton, "enabled", False)
        self._outputWorkingState.assignProperty(self.backToInputButton, "enabled", False)

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


    @pyqtSlot()
    def _updateProgressLabel(self):
        """
        Update the working progress when importing files or converting files
        """
        #import progress label
        text = str(self._importCounter.counter()) + "/" + str(self._importCounter.preset())
        self.inputProgressLabel.setText(text)

        #output progress label
        text = str(self._outputCounter.counter()) + "/" + str(self._outputCounter.preset())
        self.outputProgressLabel.setText(text)


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
    def addFolder(self):
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


    @pyqtSlot()
    def addSubfolder(self):
        """
        Import multiple files from folder and its subfolders
        """
        selectedDir = QFileDialog.getExistingDirectory(
                self,
                "Open directory",
                ".",
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)

        if not len(selectedDir) > 0:
            return

        self._importStatusMachine.postEvent(StartSearchingEvent())

        searchWorker = TdmsSearchWorker(selectedDir)
        searchWorker.signals.result.connect(self._addFiles)
        searchWorker.signals.finished.connect(self._endSearchingWrapper)

        self._threadPool.start(searchWorker)


    @pyqtSlot()
    def _endSearchingWrapper(self):
        """
        """
        #TODO: Docstring
        self._importStatusMachine.postEvent(EndSearchingEvent())


    @pyqtSlot(object)
    def _addFiles(self, filePaths):
        """
        Add multiple files into input model
        :param filePaths: [str]
        :return: None
        """
        self._importCounter.reset()
        self._importCounter.setPreset(len(filePaths))
        self._importCounter.started.emit()
        self._updateProgressLabel()

        for filePath in filePaths:
            worker = TdmsImportWorker(filePath)

            worker.signals.result.connect(self.updateSourceModel)
            worker.signals.finished.connect(self._importCounter.countUp)
            worker.signals.finished.connect(self._updateProgressLabel)

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
            self._updateProgressLabel()

            for obj in tdmsObjs:
                worker = TdmsUffWorker(obj, self.outputDir)

                worker.signals.finished.connect(self._outputCounter.countUp)
                worker.signals.finished.connect(self._updateProgressLabel)

                self._threadPool.start(worker)
