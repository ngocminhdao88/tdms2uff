# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from PyQt5.QtCore import QFileInfo
from nptdms import TdmsFile

class TdmsObj(object):
    """
    Holding informations of the tdms file
    """
    def __init__(self, path):
        self.m_path = path
        self._getFileName()
        # name, type, unit
        self.m_channels = self._getChannelInfo()

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
        if row < 0 or row >= len(self.m_channels):
            return
        return self.m_channels[row][0]

    def channelType(self, row):
        #Return channel's type at row
        if row < 0 or row >= len(self.m_channels):
            return
        return self.m_channels[row][1]

    def channelUnit(self, row):
        #Return channel's unit at row
        if row < 0 or row >= len(self.m_channels):
            return
        return self.m_channels[row][2]

    def channelUnitDesc(self, row):
        #Return channel's unit description at row
        if row < 0 or row >= len(self.m_channels):
            return
        return self.m_channels[row][3]

    def _getFileName(self):
        #Get base file name from a absolute path
        fileInfo = QFileInfo(self.m_path)
        self.m_name = fileInfo.fileName()

    def _getChannelInfo(self) -> [str]:
        #Get channel's informations from tdms file
        tdms = TdmsFile(self.m_path)
        group = tdms.groups()[0] #There is only one data group in TdmsFile
        chnObjs = tdms.group_channels(group)

        chnInfos = []
        for chnObj in chnObjs:
            properties = chnObj.properties

            chnName = chnObj.channel

            chnType = 0

            try:
                chnUnit = properties['NI_UnitDescription']
            except KeyError:
                chnUnit = "NoUnit"

            #TODO: Mapping Unit to channel type (need a list from Julian)

            chnUnitDesc = "NoDesc"

            chnInfo = [chnName, chnType, chnUnit, chnUnitDesc]

            chnInfos.append(chnInfo)
        return chnInfos

