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

from .utils import TextSplitter
from .ui.main import Ui_MainWindow
from .ui.about import Ui_AboutDialog

# delimeter for multiple paths
path_delimeter = ";"


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

    def _get_quote_dict(self):
        quote_text = self.lineQuotes.text().replace('；', ';').strip(' 　;')
        quote_list = quote_text.split(';')

        quote_dict =  { pair[0]: pair[1] for pair in quote_list }
        return quote_dict

    def _get_splitter(self):
        input_list = self.lineInput.text().strip(' 　').split(path_delimeter)
        output_path = self.lineOutput.text().strip(' 　')

        if self.rbOutputIsFolder.isChecked():
            output_is_dir = True
        else:
            output_is_dir = False

        input_enc = self.cbInputEnc.currentText().strip(' 　')
        output_enc = self.cbOutputEnc.currentText().strip(' 　')
        if "同じ" in output_enc:
            output_enc = input_enc

        _output_newline = self.cbNewline.currentText()
        if _output_newline.startswith("CRLF"):
            output_newline = "\r\n"
        elif _output_newline.startswith("LF"):
            output_newline = "\n"
        else:
            # TextSplitter will use the same newline as the input file
            output_newline = None

        delimiters = set(self.lineDelimiters.text().strip(' 　'))

        if self.checkQuote.isChecked():
            check_quote = True
        else:
            check_quote = False

        quote_dict = self._get_quote_dict()

        ts = TextSplitter(input_list=input_list,
                          output_path=output_path,
                          output_is_dir=output_is_dir,
                          input_enc = input_enc,
                          output_enc = output_enc,
                          output_newline = output_newline,
                          delimiters = delimiters,
                          check_quote = check_quote,
                          quote_dict = quote_dict)

        return ts

    def process(self):
        self.centralwidget.setDisabled(True)
        btnExecute_original_text = self.btnExecute.text()
        self.btnExecute.setText('準備中...')
        self.centralwidget.repaint()

        ts = self._get_splitter()
        print(unicode(ts))  # for debug use

        dialogProgress = QtGui.QProgressDialog("処理中", "キャンセル",
                                            0,
                                            0,
                                            parent=self)
        dialogProgress.setWindowModality(QtCore.Qt.WindowModal)

        try:
            # somehow you have to setMaximum
            # after the progress dialog is created.
            dialogProgress.setMaximum(ts.total_lines())

            self.btnExecute.setText('実行中...')
            ts.process(progress=dialogProgress)

        finally:
            self.btnExecute.setText(btnExecute_original_text)
            self.centralwidget.setEnabled(True)

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
        if len(files) != 0:
            self.lineInput.setText(path_delimeter.join(files))

    @pyqtSlot()
    def on_btnBrowseOutput_clicked(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, "フォルダを開く")
        if len(folder) != 0:
            self.lineOutput.setText(folder)

    @pyqtSlot()
    def on_btnExecute_clicked(self):
        self.process()


def main():
    import sys

    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
