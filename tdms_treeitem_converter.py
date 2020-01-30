# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from treeitem import TreeItem, NameItem, PathItem, PropertyItem
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
        nameItem = NameItem(data)

        pathItem = PathItem([tdmsObj.path()], nameItem)

        #for i in range(tdmsObj.channelsCount()):
        for chn in tdmsObj.channels():
            propertyItem = PropertyItem(chn, nameItem)

        return nameItem
