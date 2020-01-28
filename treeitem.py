# Ngoc Minh Dao
# minhdao.ngoc@linamar

class TreeItem(object):
    def __init__(data, parent=None):
        """
        Each TreeItem is constructed with a list of data and an optional parent
        """
        self._childItems = []
        self._itemData = data #list
        self._parentItem = parent

    def child(self, number):
        """
        Return a specific child from the internal list of children
        """
        if (number < 0 or number >= len(self._childItems)):
            return None
        return self._childItems[number]

    def childCount(self):
        """
        Return a total number of children
        """
        return len(self._childItems)

    def childNumber(self):
        """
        Get the index of the child in its parent's list of children.
        It accesses the parent's _childItems member directly to obtain this information:
        """
        if (self._parentItem):
            return self._parentItem.index(self)
        #The root item has no parent item. For this we return 0
        return 0

    def columnCount(self):
        """
        Return the number of elements in the internal _itemData list
        """
        retrun len(self._itemData)

    def data(self, column):
        """
        Return the data at column in the internal _itemData list
        """
        if (column < 0 or column >= len(self._itemData)):
            return None
        return self._itemData[column]

    def insertChildren(self, postion, count, columns):
        pass

    def insertColumns(self, position, columns):
        pass

    def parent(self):
        """
        Return the parent of this TreeItem
        """
        return self._parentItem

    def removeChildren(self, position, count):
        pass

    def removeColumns(self, position, columns):
        pass

    def childNumber(self):
        pass

    def setData(self, column, value):
        pass

