# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from PyQt5.QtCore import *
from tdms_item import TdmsItem

class TdmsListModel(QAbstractListModel):
    """
    Model holds the list of added tdms files
    """
    PathRole = Qt.UserRole #role to return path
    ChannelsRole = Qt.UserRole + 1 #role to return channels

    def __init__(self, parent=None):
        super(TdmsListModel, self).__init__(parent)
        self.m_tdmsItems = []

    def rowCount(self, parent=QModelIndex()):
        #Return row count in the model
        return len(self.m_tdmsItems)

    def data(self, index, role=Qt.DisplayRole):
        #Return data from model to the view
        if not index.isValid():
            return None

        row = index.row()
        if row < 0 or row >= len(self.m_tdmsItems):
            return None

        if role == Qt.DisplayRole:
            return self.m_tdmsItems[row].name()

        return None

    def addItems(self, items):
        #Add items at the end of the model
        endRow = len(self.m_tdmsItems)
        count = len(items)
        self.beginInsertRows(QModelIndex(), endRow, endRow + count - 1)
        self.m_tdmsItems.extend(items)
        self.endInsertRows()

    def removeRows(self, row, count, parent=QModelIndex()):
        #Remove rows from the model
        if row < 0 or row > len(self.m_tdmsItems):
            return False

        self.beginRemoveRows(QModelIndex(), row, row + count - 1)
        del self.m_tdmsItems[row: row + count - 1]
        self.endRemoveRows()

        return True
