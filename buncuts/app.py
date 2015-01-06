# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSlot
from .ui import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        QtGui.qApp.quit()

    @pyqtSlot()
    def on_btnBrowseInput_clicked(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "ファイルを開く")
        self.lineInput.setText(files.join(";"))

    @pyqtSlot()
    def on_btnBrowseOutput_clicked(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, "フォルダを開く")
        self.lineOutput.setText(folder)


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
