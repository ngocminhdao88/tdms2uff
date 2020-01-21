# Ngoc Minh Dao
# minhdao.ngoc@linamar

from PyQt5.QtWidgets import QDialog
from view import Ui_Dialog

class ViewController(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        #setup the gui
        super(ViewController, self).__init__(parent)
        self.setupUi(self)
