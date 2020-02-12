#Ngoc Minh Dao
#minhdao.ngoc@linamar.com

from PyQt5.QtCore import *

class StartSearchingEvent(QEvent):
    def __init__(self):
        super(StartSearchingEvent, self).__init__(QEvent.Type(QEvent.User + 2))


class EndSearchingEvent(QEvent):
    def __init__(self):
        super(EndSearchingEvent, self).__init__(QEvent.Type(QEvent.User + 3))


class StartSearchingTransition(QAbstractTransition):
    def eventTest(self, e):
        return e.type() == QEvent.User + 2

    def onTransition(self, e):
        pass


class EndSearchingTransition(QAbstractTransition):
    def eventTest(self, e):
        return e.type() == QEvent.User + 3

    def onTransition(self, e):
        pass
