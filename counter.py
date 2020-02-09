#Ngoc Minh Dao
#minhdao.ngoc@linamar.com

from PyQt5.QtCore import pyqtSignal, QObject

class Counter(QObject):
    """
    A simple counter class
    """
    tripped = pyqtSignal()
    started = pyqtSignal()

    def __init__(self, counter=0, preset=0):
        self._counter = counter
        self._preset = preset

    def preset(self):
        """
        Get counter's preset value
        :return: int
        """
        return self._preset

    def setPreset(self, preset):
        """
        Set the counter's preset value to new value
        :param preset: int
        :return: None
        """
        if preset != self._preset:
            self._preset = preset

    def counter(self):
        """
        Get counter current value
        :return: int
        """
        return self._counter

    def setCounter(self, counter):
        """
        Set the counter to new value
        :param counter: int
        :return: None
        """
        if counter != self._counter:
            self._counter = counter

    def countUp(self):
        """
        Increase the counter number by one.
        The 'tripped' signal will be emitted when the counter is greater
        or equal the preset value
        :return: None
        """
        self._counter += 1

        if self._counter >= self._preset:
            self.tripped.emit()

    def countDown(self):
        """
        decrease the counter number by one
        The 'tripped' signal will be emitted when the counter is less than
        or equal the preset value
        :return: None
        """
        self._counter -= 1

        if self._counter <= self._preset:
            self.tripped.emit()

    def reset(self):
        """
        reset this counter
        :return: None
        """
        self._counter = 0

