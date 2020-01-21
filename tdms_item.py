# Ngoc Minh Dao
# minhdao.ngoc@linamar

import os

class TdmsItem():
    def __init__(self, path):
        self.m_path = path
        self.m_name = ""
        self.m_channels = [[]] # name, type, unit
        self.m_channelColumnCount = 3

    def name(self):
        #Return the name of tdms file
        return self.m_name

    def path(self):
        #Return the absolute path of tdms file
        return self.m_path

    def channelCount(self):
        #Return number of channels this item has
        return len(self.m_channels)

    def columnCount(self):
        #Return number of columns of data in item's channel
        return self.m_channelColumnCount

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

    def channelType(self, row):
        #Return channel's unit at row
        if (row < 0 or row >= len(self.m_channels)):
            return
        return self.m_channels[row][2]

    def _getFileName(self):
        #Get base file name from a absolute path
        self.m_name = os.path.basename(self.path)
