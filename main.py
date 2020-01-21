# Ngoc Minh Dao
# minhdao.ngoc@linamar.com

from PyQt5.QtWidgets import QApplication
from view_controller import ViewController

if __name__ == "__main__":
    #lauch the application
    app = QApplication([])

    wnd = ViewController()
    wnd.setWindowTitle("TMDS->UFF58 converter")
    wnd.show()

    app.exec_()
