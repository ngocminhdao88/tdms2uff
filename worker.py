from PyQt5.QtCore import *
from tdmsobj import TdmsObj
from converter import *
from convert import Convert

class WorkerSignals(QObject):
    started = pyqtSignal()
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
        self._converter.convert_tdms()
        self.signals.finished.emit()


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

class TdmsSearchWorker(QRunnable):
    """
    Worker that searching for tdms files in sub directory
    """
    def __init__(self, rootPath):
        super(TdmsSearchWorker, self).__init__()
        self.signals = WorkerSignals()
        self._rootPath = rootPath
        self._filePaths = []

    @pyqtSlot()
    def run(self):
        """
        Search for all tdms files in subdirectories from the rootPath
        """
        it = QDirIterator(self._rootPath, ["*.tdms"], QDir.NoFilter, QDirIterator.Subdirectories)
        self.signals.started.emit()

        while it.hasNext():
            self._filePaths.append(it.next())

        self.signals.result.emit(self._filePaths)
        self.signals.finished.emit()

