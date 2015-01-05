#!/usr/bin/env python2
# coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from PyQt4 import QtGui, QtCore
from buncuts import app_rc

assert app_rc  # just silent PEP8


class BunCutsWindow(QtGui.QWidget):
    def __init__(self):
        super(BunCutsWindow, self).__init__()

        self.initUI()
        self.initBtn()

        self.show()

    def initUI(self):
        self.setWindowTitle('BunCuts - 文割')
        self.setWindowIcon(QtGui.QIcon(':/img/icon.256.png'))
        # self.setGeometry(300, 300, 400, 300)

    def initBtn(self):
        btn = QtGui.QPushButton('終了', self)
        btn.setToolTip("アプリを閉じます")

        btn.clicked.connect(
            QtCore.QCoreApplication.instance().quit)

        btn.resize(btn.sizeHint())
        btn.move(150, 100)

    def center(self):
        rec = self.frameGeometry()
        center_point = QtGui.QDesktopWidget().availableGeometry().center()
        rec.moveCenter(center_point)
        self.move(rec.topLeft())


def main():
    app = QtGui.QApplication(sys.argv)

    font = QtGui.QFont()
    # Wow, you can actually define a comma separated list of font families.
    font.setFamily('Segoe UI, Meiryo')
    font.setStyleHint(QtGui.QFont.SansSerif)
    app.setFont(font)

    win = BunCutsWindow()
    win.center()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
