#encoding=utf8
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class TimerMessageBox(QtGui.QMessageBox):
    def __init__(self, timeout=3, parent=None, userMessage=''):
        super(TimerMessageBox, self).__init__(parent)
        self.setWindowTitle(_translate("Dialog", "秤信息", None))
        self.time_to_wait = timeout
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        self.setFont(font)
        self.setText(_translate("Dialog", userMessage, None))
        self.setStandardButtons(QtGui.QMessageBox.NoButton)
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.onChangeContent)
        self.timer.start()

    def onChangeContent(self):
        # self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()
        btn = QtGui.QPushButton('Button', self)
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        self.setWindowTitle('Example')
        btn.clicked.connect(self.warning)

    def warning(self):
        messagebox = TimerMessageBox(5, self)
        messagebox.exec_()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

