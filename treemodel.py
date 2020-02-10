# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtCore import *
from treeitem import TreeItem

class TreeModel(QAbstractItemModel):
    #Roles to filter input and output view
    Item_Role = Qt.UserRole

    def __init__(self, headers, data, parent=None) -> None:
        super(TreeModel, self).__init__(parent)

        rootData = []
        for header in headers:
            rootData.append(header)

        self._rootItem = TreeItem(rootData)

        #self._setupModelData(data.split('\n'), self._rootItem)

    def rootItem(self) -> TreeItem:
        """
        Return the root item of this model
        """
        return self._rootItem

    def getItem(self, index) -> TreeItem:
        """
        Return the TreeItem from model using the index
        """
        if index.isValid():
            item = index.internalPointer()
            if item:
                return item
        return self._rootItem

    def data(self, index, role) -> object:
        """
        Return data from model to the view
        """
        if not index.isValid():
            return None

        item = self.getItem(index)

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return item.data(index.column())

        if role == TreeModel.Item_Role:
            return item

        return QVariant()


    def headerData(self, section, orientation, role) -> object:
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._rootItem.data(section)

    def index(self, row, column, parent=QModelIndex()) -> QModelIndex:
        """
        Obtain model indexes corresponding to children of given parent item
        """
        #Only return model indexes for child items if the parent index in invalid (root item)
        #or if it has a zero column number
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parentItem = self.getItem(parent)
        if not parentItem:
            return QModelIndex()

        #Create a model index to uniquely with the row and column numbers
        #and a pointer to the item
        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)

        return QModelIndex()

    def parent(self, index) -> QModelIndex:
        """
        Return the model indexes for parents of item by finding the correspoinding item for a
        give model index, using its parent() function to obtain its parent item, then
        creating a model index to represent the parent.

        Item without parents, including the root item, are handled by returning a null model index.
        Otherwise, a model index ins created and returned as in the index() function, with a suitable row number,
        but with a zero column
        """
        if not index.isValid():
            return QModelIndex()

        childItem = self.getItem(index)
        parentItem = None
        if childItem:
            parentItem = childItem.parent()

        if parentItem == self._rootItem or not parentItem:
            return QModelIndex()

        return self.createIndex(parentItem.childNumber(), 0, parentItem)


    def rowCount(self, parent=QModelIndex()) -> int:
        """
        Return the children that parent has
        """
        parentItem = self.getItem(parent)

        if parentItem:
            return parentItem.childCount()
        else:
            return 0


    def columnCount(self, parent=QModelIndex()) -> int:
        """
        All items are defined to have the same number of columns associated with them
        """
        return self._rootItem.columnCount()

    def flags(self, index) -> Qt.ItemFlags:
        """
        Return flags ItemIsEditable, ItemIsSelectable and ItemIsEnable to be able to edit and select item
        """
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled


    def setData(self, index, value, role=Qt.EditRole) -> bool:
        """
        Set data from view back to the model
        """
        if role != Qt.EditRole:
            return False

        item = self.getItem(index)
        result = item.setData(index.column(), value)

        if result:
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])

        return result

    def setHeaderData(self, section, orientation, value, role=Qt.EditRole) -> bool:
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result = self._rootItem.setData(section, value)

        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def insertColumns(self, position, columns, parent=QModelIndex()) -> bool:
        """
        Insert columns into the model
        """
        self.beginInsertColumns(parent, position, position + columns - 1)
        success = self._rootItem.insertColumns(position, columns)
        self.endInsertColumns()

        return success

    def removeColumns(self, position, columns, parent=QModelIndex()) -> bool:
        """
        Remove columns from the model
        """
        self.beginRemoveColumns(parent, position, position + columns - 1)
        success = self._rootItem.removeColumns(position, columns)
        self.endRemoveColumns()

        if self._rootItem.columnCount() == 0:
            self.removeRows(0, self.rowCount())

        return success

    def insertRows(self, position, rows, parent=QModelIndex()) -> bool:
        """
        Insert rows into model
        """
        parentItem = self.getItem(parent)
        if not parentItem:
            return False

        self.beginInsertRows(parent, position, position + rows - 1)
        success = parentItem.insertChildren(position, rows, self._rootItem.columnCount())
        self.endInsertRows()

        return success

    def removeRows(self, position, rows, parent=QModelIndex()) -> bool:
        """
        Remove rows from model
        """
        parentItem = self.getItem(parent)
        if not parentItem:
            return False

        self.beginRemoveRows(parent, position, position + rows - 1)
        success = parentItem.removeChildren(position, rows)
        self.endRemoveRows()

        return success
