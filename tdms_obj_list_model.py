# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from PyQt5.QtCore import *

class TdmsObj(object):
    """
    Holding informations of the tdms file
    """
    def __init__(self, path):
        self.m_path = path
        self._getFileName()
        self.m_channels = [[]] # name, type, unit

    def name(self):
        #Return the name of tdms file
        return self.m_name

    def path(self):
        #Return the absolute path of tdms file
        return self.m_path

    def channelCount(self):
        #Return number of channels this item has
        return len(self.m_channels)

    def channels(self):
        #Return channels of this tdms file
        return self.m_channels

    def channelName(self, row):
        #Return channel's name at row
        if (row < 0 or row >= len(self.m_channels)):
            return
        return self.m_channels[row][0]

    def channelType(self, row):
        #Return channel's type at row
        if (row < 0 or row >= len(self.m_channels)):
            return
        return self.m_channels[row][1]

    def channelUnit(self, row):
        #Return channel's unit at row
        if (row < 0 or row >= len(self.m_channels)):
            return
        return self.m_channels[row][2]

    def _getFileName(self):
        #Get base file name from a absolute path
        fileInfo = QFileInfo(self.m_path)
        self.m_name = fileInfo.fileName()

class TdmsObjListModel(QAbstractListModel):
    """
    Model holds the list of added tdms files
    """
    ObjRole = Qt.UserRole #role to return path

    def __init__(self, parent=None):
        super(TdmsObjListModel, self).__init__(parent)
        self.m_tdmsObjs = []

    def rowCount(self, parent=QModelIndex()):
        #Return row count in the model
        return len(self.m_tdmsObjs)

    def data(self, index, role=Qt.DisplayRole):
        #Return data from model to the view
        if not index.isValid():
            return None

        row = index.row()
        if row < 0 or row >= len(self.m_tdmsObjs):
            return None

        if role == Qt.DisplayRole:
            return self.m_tdmsObjs[row].name()

        if role == TdmsObjListModel.ObjRole:
            return self.m_tdmsObjs[row]

        return None

    def addTdmsObjs(self, tdmsObjs):
        #Add tdms objects at the end of the model
        row = len(self.m_tdmsObjs)
        count = len(tdmsObjs)

        self.beginInsertRows(QModelIndex(), row, row + count - 1)
        self.m_tdmsObjs.extend(tdmsObjs)
        self.endInsertRows()

    def removeRow(self, row, parent=QModelIndex()):
        #Remove row from the model
        if row < 0 or row > len(self.m_tdmsObjs):
            return False

        self.beginRemoveRows(QModelIndex(), row, row)
        self.m_tdmsObjs.pop(row)
        self.endRemoveRows()

        return True
