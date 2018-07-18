# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainMenu_Prot.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys

# import os
# from PyQt4 import *
# from PyQt4.Qt import QPluginLoader
from PyQt4 import QtCore, QtGui


import TextTool
import CopyTool
from Ip4 import MyDialog, MyFont, resource_path

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


class Ui_DigiToolDialog(object):

    def on_btn_texttool(self):
        self.Dialog = MyDialog(self.main_dialog)
        self.Dialog.setParams(self.main_dialog.getParams())
        global ui1
        ui1 = TextTool.Ui_TextToolDialog()
        # self.Dialog.setModal(True)
        # self.Dialog.show()
        ui1.setupUi(self.Dialog)
        # self.Dialog.show()
        self.Dialog.exec_()

    def on_btn_copytool(self):
        self.Dialog = MyDialog(self.main_dialog)
        self.Dialog.setParams(self.main_dialog.getParams())
        global ui1
        ui1 = CopyTool.Ui_CopyToolDialog()
        # self.Dialog.show()
        # self.Dialog.setModal(True)
        ui1.setupUi(self.Dialog)
        # self.Dialog.show()
        self.Dialog.exec_()

    def setupUi(self, dialog):

        # QPlugin = QPluginLoader("qico4.dll")
        # print QPlugin
        # base_path = os.path.abspath(".")
        # icon_file_path = os.path.join(base_path, "bi.ico")
        # print icon_file_path
        # icon = QtGui.QIcon(resource_path("as.ico"))
        # icon = QtGui.QIcon("as.ico")
        icon_file_path = resource_path("as.png")
        icon = QtGui.QIcon(icon_file_path)
        # icon.addPixmap(QtGui.QPixmap(_fromUtf8(resource_path("as.ico"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # icon.addPixmap(QtGui.QPixmap(_fromUtf8("as.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # icon.addFile(_fromUtf8(icon_file_path))
        dialog.setWindowIcon(icon)
        # print QtCore.QLocale().system().name()

        dialog.setObjectName(_fromUtf8("dialog"))
        dialog.resize(356, 243)

        self.btn_texttool = QtGui.QPushButton(dialog)
        self.btn_texttool.setGeometry(QtCore.QRect(75, 45, 196, 46))
        self.btn_texttool.setObjectName(_fromUtf8("btn_texttool"))
        self.btn_texttool.setFont(MyFont())
        self.btn_copytool = QtGui.QPushButton(dialog)
        self.btn_copytool.setGeometry(QtCore.QRect(75, 120, 196, 46))
        self.btn_copytool.setObjectName(_fromUtf8("btn_copytool"))
        self.btn_copytool.setFont(MyFont())

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

        self.btn_texttool.clicked.connect(self.on_btn_texttool)
        self.btn_copytool.clicked.connect(self.on_btn_copytool)

        self.main_dialog = dialog

        from TimerMessageBox import TimerMessageBox
        messagebox = TimerMessageBox(2, dialog, userMessage="当前秤型号为: " + dialog.getParams()["scaleType"])
        messagebox.exec_()



    def retranslateUi(self, dialog):
        dialog.setWindowTitle(_translate("dialog", "寺冈秤工具主菜单", None))
        self.btn_texttool.setText(_translate("dialog", "文本下发特定工具", None))
        self.btn_copytool.setText(_translate("dialog", "数据复制工具", None))


if __name__ == "__main__":
    # import ui.icon_rc
    # ui.icon_rc.qInitResources()

    app = QtGui.QApplication(sys.argv)
    dialog = QtGui.QDialog()
    ui = Ui_DigiToolDialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

