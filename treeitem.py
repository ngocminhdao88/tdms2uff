# Ngoc Minh Dao
# minhdao.ngoc@linamar

class TreeItem(object):
    def __init__(self, data, parent=None):
        """
        Each TreeItem is constructed with a list of data and an optional parent
        """
        self._childItems = []
        self._itemData = data #list
        self._parentItem = parent

        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return "Item"

    def child(self, number):
        """
        Return a specific child from the internal list of children
        """
        if (number < 0 or number >= len(self._childItems)):
            return None
        return self._childItems[number]

    def childCount(self) -> int:
        """
        Return a total number of children
        """
        return len(self._childItems)

    def childNumber(self) -> int:
        """
        Get the index of the child in its parent's list of children.
        It accesses the parent's _childItems member directly to obtain this information:
        """
        if (self._parentItem):
            return self._parentItem._childItems.index(self)
        #The root item has no parent item. For this we return 0
        return 0

    def columnCount(self) -> int:
        """
        Return the number of elements in the internal _itemData list
        """
        return len(self._itemData)

    def data(self, column):
        """
        Return the data at column in the internal _itemData list
        """
        if (column < 0 or column >= len(self._itemData)):
            return None
        return self._itemData[column]

    def setData(self, column, value) -> bool:
        """
        Store values in the _itemData list for valid indexes
        """
        if (column < 0 or column >= len(self._itemData)):
            return False

        self._itemData[column] = value
        return True

    def addChild(self, child) -> None:
        """
        Add a child into _childItems
        """
        self._childItems.append(child)

    def insertChildren(self, position, count, columns) -> bool:
        """
        Add new child into the _childItems list
        """
        if (position < 0 or position > len(self._childItems)):
            return False

        for i in range(count):
            data = [None] * columns
            item = TreeItem(data, self)
            self._childItems.insert(position, item)
        return True

    def removeChildren(self, position, count) -> bool:
        """
        Remove children item from the internal list
        """
        if (position < 0 or position + count > len(self._childItems)):
            return False

        for i in range(count):
            child = self._childItems.pop(position)
            child.setParent(None)

        return True

    def parent(self):
        """
        Return the parent of this TreeItem
        """
        return self._parentItem

    def setParent(self, parent=None):
        """
        Set the parent to this TreeItem
        """
        self._parentItem = parent


    def insertColumns(self, position, columns) -> bool:
        """
        This function are expected to be called on every item in the tree.
        This is done by recursively calling this function on each child of the item
        """
        if (position < 0 or position > len(self._itemData)):
            return False

        for i in range(columns):
            self._itemData.insert(position, 0)

        for child in self._childItems:
            child.insertColumns(position, columns)

        return True

    def removeColumns(self, position, columns) -> bool:
        if (position < 0 or position + columns > len(self._itemData)):
            return False

        for i in range(columns):
            del self._itemData[position]

        for child in self._childItems:
            child.removeColumns(position, columns)

    def _log(self, tabLevel=-1) -> str:
        """
        Printout the tree structure
        """
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += '\t'

        output += "|- " + self._itemData[0] + '\n'

        for childItem in self._childItems:
            output += childItem._log(tabLevel)

        tabLevel -= 1

        return output

    def __repr__(self):
        return self._log()


class NameItem(TreeItem):
    def __init__(self, data, parent=None):
        super(NameItem, self).__init__(data, parent)

    def typeInfo(self):
        return "NameItem"

class PathItem(TreeItem):
    def __init__(self, data, parent=None):
        super(PathItem, self).__init__(data, parent)

    def typeInfo(self):
        return "PathItem"

class PropertyItem(TreeItem):
    def __init__(self, data, parent=None):
        super(PropertyItem, self).__init__(data, parent)

    def typeInfo(self):
        return "PropertyItem"
