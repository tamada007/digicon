# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

from ui import TextTool
from ui import CopyTool
from ui.Ip4 import MyDialog

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


class Ui_dialog(object):

    def on_btn_texttool(self):
        self.Dialog = MyDialog()
        ui = TextTool.Ui_TextToolDialog()
        ui.setupUi(self.Dialog)
        self.Dialog.show()

    def on_btn_copytool(self):
        self.Dialog = MyDialog()
        ui = CopyTool.Ui_CopyToolDialog()
        ui.setupUi(self.Dialog)
        self.Dialog.show()

    def setupUi(self, dialog):
        dialog.setObjectName(_fromUtf8("dialog"))
        dialog.resize(356, 243)
        self.btn_texttool = QtGui.QPushButton(dialog)
        self.btn_texttool.setGeometry(QtCore.QRect(75, 45, 196, 46))
        self.btn_texttool.setObjectName(_fromUtf8("btn_texttool"))
        self.btn_copytool = QtGui.QPushButton(dialog)
        self.btn_copytool.setGeometry(QtCore.QRect(75, 120, 196, 46))
        self.btn_copytool.setObjectName(_fromUtf8("btn_copytool"))

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)


        self.btn_texttool.clicked.connect(self.on_btn_texttool)
        self.btn_copytool.clicked.connect(self.on_btn_copytool)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(_translate("dialog", "寺冈秤工具主菜单", None))
        self.btn_texttool.setText(_translate("dialog", "文本下发特定工具", None))
        self.btn_copytool.setText(_translate("dialog", "数据复制工具", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    dialog = QtGui.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

