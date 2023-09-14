import os
import sys
from pathlib import Path

from findPathWidget import FindPathWidget
from script import convert_searchable_pdf_to_text, convert_img_to_text

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QWidget, QTableWidget, \
    QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    onSucceed = pyqtSignal(int, bool)

    def __init__(self, filenames):
        super(Thread, self).__init__()
        self.__filenames = filenames

    def run(self):
        try:
            dst_dirname = 'dst'
            os.makedirs(dst_dirname, exist_ok=True)
            for i, filename in enumerate(self.__filenames):
                try:
                    file_type = Path(filename).suffix
                    print(file_type)
                    if file_type in ['.pdf']:
                        convert_searchable_pdf_to_text(filename, True)
                    if file_type in ['.png', '.jpg']:
                        convert_img_to_text(filename, True)
                    self.onSucceed.emit(i, True)
                except Exception as e:
                    print(e)
                    self.onSucceed.emit(i, False)
        except Exception as e:
            print(e)
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initUi()

    def __initUi(self):
        self.setWindowTitle('PDF convertor')

        findPathWidget = FindPathWidget()
        findPathWidget.setAsDirectory(True)
        findPathWidget.added.connect(self.__added)

        self.__btn = QPushButton('Convert')
        self.__btn.clicked.connect(self.__run)

        self.__tableWidget = QTableWidget()
        self.__tableWidget.setColumnCount(2)
        self.__tableWidget.setHorizontalHeaderLabels(['Name', 'Complete'])
        self.__tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        lay = QVBoxLayout()
        lay.addWidget(findPathWidget)
        lay.addWidget(self.__btn)
        lay.addWidget(self.__tableWidget)
        lay.setAlignment(Qt.AlignTop)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)
        self.setCentralWidget(mainWidget)

        self.__btn.setEnabled(False)

    def __added(self, dirname):
        dirname = Path(dirname)
        for item in dirname.glob('*'):
            if item.suffix.lower() in ['.pdf', '.jpg', '.png']:
                item = QTableWidgetItem(str(item.resolve()))
                item.setTextAlignment(Qt.AlignCenter)
                r_idx = self.__tableWidget.rowCount()
                self.__tableWidget.setRowCount(r_idx+1)
                self.__tableWidget.setItem(r_idx, 0, item)
        self.__btn.setEnabled(True)

    def __run(self):
        filenames = [self.__tableWidget.item(i, 0).text() for i in range(self.__tableWidget.rowCount())]
        self.__t = Thread(filenames)
        self.__t.started.connect(self.__started)
        self.__t.onSucceed.connect(self.__onSucceed)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __onSucceed(self, i, f):
        res = 'Success' if f else 'Failed'
        item = QTableWidgetItem(res)
        item.setTextAlignment(Qt.AlignCenter)
        self.__tableWidget.setItem(i, 1, item)

    def __started(self):
        print('started')

    def __finished(self):
        print('finished')


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())