# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from treeitem import *
from tdmsobj import TdmsObj

class TdmsTreeItemConverter(object):
    def __init__(self):
        pass

    def toTdmsObj(self, item: TreeItem, columns=1) -> TdmsObj:
        """
        Convert a TreeItem object to a tdms object
        """
        #input is not valid
        if not item:
            return None

        tdmsObj = TdmsObj()

        tdmsObj.setPath(item.data(1)) #path

        chns = []
        for chn in item.children():
            chns.append(chn.itemData())

        tdmsObj.setChannels(chns)

        return tdmsObj


    def toTreeItem(self, tdmsObj: TdmsObj, columns=2, parent=None) -> TreeItem:
        """
        Convert a tdms object to a TreeItem object.
        The outputed TreeItem can be added directy to the parent item
        """

        if not TdmsObj:
            return None

        #construct the DataSetItem
        data = [None] * columns
        data[0] = tdmsObj.name()
        data[1] = tdmsObj.path()

        dataSetItem = DataSetItem(data, parent)

        #add all channels
        for chn in tdmsObj.channels():
            chnItem = ChannelItem(chn, dataSetItem)

        return dataSetItem
