# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from treeitem import TreeItem
from tdmsobj import TdmsObj

class TdmsTreeItemConverter(object):
    def __init__(self):
        pass

    def toTdmsObj(self, item: TreeItem, columns=1) -> TdmsObj:
        """
        Convert a TreeItem object to a tdms object
        """
        #TODO: need to see example from QT
        pass

    def toTreeItem(self, tdmsObj: TdmsObj, columns=1) -> TreeItem:
        """
        Convert a tdms object to a TreeItem object
        """

        if not TdmsObj:
            return None

        #construct the name item
        data = [None] * columns
        for i in range(columns):
            data[i] = tdmsObj.name()
        nameItem = TreeItem(data)

        nameItem.insertChildren(0, 2, columns)

        pathItem = nameItem.child(0)
        pathItem.setData(0, tdmsObj.path())

        proItem = nameItem.child(1)
        proItem.setData(0, "properties")

        proItem.insertChildren(0, tdmsObj.channelsCount(), tdmsObj.channelLength())

        for i in range(tdmsObj.channelsCount()):
            item = proItem.child(i)

            item.setData(0, tdmsObj.channelName(i))
            item.setData(1, tdmsObj.channelType(i))
            item.setData(2, tdmsObj.channelUnit(i))
            item.setData(3, tdmsObj.channelUnitDesc(i))

        return nameItem
