#!/usr/bin/env python2
# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSlot
from buncuts.ui import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

    @pyqtSlot()
    def on_btnExit_clicked(self):
        QtCore.QCoreApplication.instance().quit()


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
