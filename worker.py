from PyQt5.QtCore import *
from tdmsobj import TdmsObj
from converter import *
from convert import Convert

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(object)
    result = pyqtSignal(object)

class TdmsUffWorker(QRunnable):
    """
    Worker thread that convert tdms file to uff file

    """
    def __init__(self, tdmsObj: TdmsObj, outputPath: str):
        super(TdmsUffWorker, self).__init__()
        self._outputPath = outputPath
        self._tdmsObj = tdmsObj
        self.signals = WorkerSignals()
        self._converter = Convert(tdmsObj)

    @pyqtSlot()
    def run(self):
        """
        Convertion code goes in this function
        """
        print("Thread start")
        self._converter.convert_tdms()

class TdmsImportWorker(QRunnable):
    """
    Worker thread that help read big tdms file
    """
    def __init__(self, filePath):
        super(TdmsImportWorker, self).__init__()
        self._filePath = filePath
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Read the tmds file from given path.
        A result signal will be emited at the end
        """
        fileInfo = QFileInfo(self._filePath)
        if not fileInfo.exists():
            self.signals.error.emit("File not found")
            return

        fileName = fileInfo.fileName()
        tdmsObj = TdmsObj(self._filePath)

        converter = TdmsTreeItemConverter()

        item = converter.toTreeItem(tdmsObj, 4)

        self.signals.result.emit(item)
        self.signals.finished.emit()

