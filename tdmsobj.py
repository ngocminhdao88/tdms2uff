# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from PyQt5.QtCore import QFileInfo
from nptdms import TdmsFile
from treeitem import TreeItem
import json

class TdmsObj(object):
    """
    Holding informations of the tdms file
    """
    def __init__(self, path=""):
        self._path = path
        self._name = self._getFileName()
        # name, type, unit
        self._channels = self._getChannelInfo()

    def name(self):
        #Return the name of tdms file
        return self._name

    def path(self):
        #Return the absolute path of tdms file
        return self._path

    def setPath(self, path):
        """
        Set the path to tdms file
        """
        if self._path != path:
            self._path = path
            self._name = self._getFileName()

    def channelsCount(self):
        #Return number of channels this item has
        return len(self._channels)

    def channelLength(self):
        """
        Return the length of a channel
        """
        if len(self._channels) > 0:
            return len(self._channels[0])
        return 0

    def channels(self):
        #Return channels of this tdms file
        return self._channels

    def setChannels(self, channels):
        """
        Set the channels for this tdms object
        """
        if channels != self._channels:
            self._channels = channels

    def channelName(self, row):
        #Return channel's name at row
        if row < 0 or row >= len(self._channels):
            return
        return self._channels[row][0]

    def channelType(self, row):
        #Return channel's type at row
        if row < 0 or row >= len(self._channels):
            return
        return self._channels[row][1]

    def channelUnit(self, row):
        #Return channel's unit at row
        if row < 0 or row >= len(self._channels):
            return
        return self._channels[row][2]

    def channelUnitDesc(self, row):
        #Return channel's unit description at row
        if row < 0 or row >= len(self._channels):
            return
        return self._channels[row][3]

    def _getFileName(self) -> str:
        #Get base file name from a absolute path
        fileInfo = QFileInfo(self._path)

        if not fileInfo.exists():
            return ""
        else:
            return fileInfo.fileName()

    def _getChannelInfo(self) -> [[object]]:
        #Get channel's informations from tdms file

        #load units from units.json file
        f = open("units.json", 'r')
        units = json.load(f)
        f.close()

        fileInfo = QFileInfo(self._path)
        if not fileInfo.exists():
            return [[]]

        tdms = TdmsFile(self._path)
        group = tdms.groups()[0] #There is only one data group in TdmsFile
        chnObjs = tdms.group_channels(group)

        chnInfos = []
        for chnObj in chnObjs:
            properties = chnObj.properties

            chnName = chnObj.channel

            try:
                chnUnit = properties['NI_UnitDescription']
            except KeyError:
                chnUnit = "unknown"

            try:
                chnType = units[chnUnit]["number"]
                chnUnitDesc = units[chnUnit]["unit_desc"]
            except KeyError:
                chnType = 0
                chnUnitDesc = "unknown"

            chnInfo = [chnName, chnType, chnUnit, chnUnitDesc]

            chnInfos.append(chnInfo)
        return chnInfos
