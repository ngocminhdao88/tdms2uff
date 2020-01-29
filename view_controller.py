# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from view import Ui_Dialog
from tdmsobj import TdmsObj
from treeitem import TreeItem
from treemodel import TreeModel

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)

        self.outputDir = ""

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

        model = index.model() #proxymodel
        sourceModel = model.sourceModel()
        sourceIndex = model.mapToSource(index)
        propertyIndex = sourceModel.index(1, 0, sourceIndex)

        #TODO: not working when input are filtered
        proxyIndex = model.mapFromSource(propertyIndex)
        self.channelsTreeView.setRootIndex(proxyIndex)

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

        for filePath in filePaths:
            fileInfo = QFileInfo(filePath)
            fileName = fileInfo.fileName()
            tdmsObj = TdmsObj(filePath)
            #print(tdmsObj.channels())

            #index = self.inputListView.selectionModel().currentIndex()
            model = self.inputListView.model()
            sourceModel = model.sourceModel()
            #sourceIndex = model.mapToSource(index)

            """
            if not sourceModel.insertRow(sourceIndex.row() + 1, sourceIndex.parent()):
                return
            childIndex = sourceModel.index(sourceIndex.row() + 1, 0, sourceIndex.parent())
            sourceModel.setData(childIndex, fileName)

            if not sourceModel.insertRows(0, 2, childIndex):
                return
            child = sourceModel.index(0, 0, childIndex)
            sourceModel.setData(child, filePath)
            child = sourceModel.index(1, 0, childIndex)
            sourceModel.setData(child, "properties")

            if not sourceModel.insertRow(0, child):
                return
            propertyIndex = sourceModel.index(0, 0, child)
            sourceModel.setData(propertyIndex, "tacho")
            propertyIndex = sourceModel.index(0, 1, child)
            sourceModel.setData(propertyIndex, 21)
            propertyIndex = sourceModel.index(0, 2, child)
            sourceModel.setData(propertyIndex, "V")
            propertyIndex = sourceModel.index(0, 3, child)
            sourceModel.setData(propertyIndex, "Voltage")
            """

            #item = sourceModel.getItem(sourceIndex)
            item = sourceModel.rootItem() #rootitem
            sourceModel.layoutAboutToBeChanged.emit() #start changing model layout

            item.insertChildren(0, 1, 4) #fileName item
            item = item.child(0) #filename
            item.setData(0, fileName)


            item.insertChildren(0, 2, 4)
            pathItem = item.child(0)
            pathItem.setData(0, filePath)

            propertyItem = item.child(1)
            propertyItem.setData(0, "properties")

            chnNum = tdmsObj.channelCount()
            propertyItem.insertChildren(0, chnNum, 4)

            for i in range(chnNum):
                subPropertyItem = propertyItem.child(i)

                subPropertyItem.setData(0, tdmsObj.channelName(i))
                subPropertyItem.setData(1, tdmsObj.channelType(i))
                subPropertyItem.setData(2, tdmsObj.channelUnit(i))
                subPropertyItem.setData(3, tdmsObj.channelUnitDesc(i))

            sourceModel.layoutChanged.emit() #end changing model layout

            print(item) #printout roottree model


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
