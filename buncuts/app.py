# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# select PyQt API v2
import sip
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot

from . import utils
from .ui.main import Ui_MainWindow
from .ui.about import Ui_AboutDialog


class AboutDialog(QtGui.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None, flags=0):
        QtGui.QDialog.__init__(self, parent, flags)
        self.setupUi(self)

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.accept()


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

    @pyqtSlot()
    def on_actionExit_triggered(self):
        QtGui.qApp.quit()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        flagNoHelp = (QtCore.Qt.WindowSystemMenuHint |
                      QtCore.Qt.WindowTitleHint)
        AboutDialog(parent=self, flags=flagNoHelp).exec_()

    @pyqtSlot()
    def on_btnBrowseInput_clicked(self):
        files = QtGui.QFileDialog.getOpenFileNames(self, "ファイルを開く")
        self.lineInput.setText(";".join(files))

    @pyqtSlot()
    def on_btnBrowseOutput_clicked(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, "フォルダを開く")
        self.lineOutput.setText(folder)

    @pyqtSlot()
    def on_btnExecute_clicked(self):
        utils.split_into_sentences(text=self.lineInput.text(),
                                   output=self.lineOutput.text(),
                                   is_dir=True)


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
