# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectScale_Prot.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from Ip4 import MyDialog, MyFont, resource_path
from DigiToolMenu import Ui_DigiToolDialog

from common import common

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

class Ui_Dialog_Choose_Scale_Type(object):

    def on_btn_sm110(self):
        self.Dialog = MyDialog(self.main_dialog)
        self.Dialog.setParams({"scaleType": "sm110"})
        global ui1
        ui1 = Ui_DigiToolDialog()
        ui1.setupUi(self.Dialog)
        # self.Dialog.show()
        self.Dialog.exec_()

    def on_btn_sm120(self):
        self.Dialog = MyDialog(self.main_dialog)
        self.Dialog.setParams({"scaleType": "sm120"})
        global ui1
        ui1 = Ui_DigiToolDialog()
        ui1.setupUi(self.Dialog)
        # self.Dialog.show()
        self.Dialog.exec_()

    def setupUi(self, Dialog_Choose_Scale_Type):

        self.main_dialog = Dialog_Choose_Scale_Type

        icon_file_path = resource_path("as.png")
        icon = QtGui.QIcon(icon_file_path)
        Dialog_Choose_Scale_Type.setWindowIcon(icon)

        Dialog_Choose_Scale_Type.setObjectName(_fromUtf8("Dialog_Choose_Scale_Type"))
        Dialog_Choose_Scale_Type.resize(484, 323)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog_Choose_Scale_Type)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(15, 90, 451, 136))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.btn_sm110 = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sm110.sizePolicy().hasHeightForWidth())
        self.btn_sm110.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(26)
        self.btn_sm110.setFont(font)
        self.btn_sm110.setObjectName(_fromUtf8("btn_sm110"))
        self.verticalLayout.addWidget(self.btn_sm110)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btn_sm120 = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_sm120.sizePolicy().hasHeightForWidth())
        self.btn_sm120.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(26)
        self.btn_sm120.setFont(font)
        self.btn_sm120.setObjectName(_fromUtf8("btn_sm120"))
        self.verticalLayout.addWidget(self.btn_sm120)

        self.retranslateUi(Dialog_Choose_Scale_Type)
        QtCore.QMetaObject.connectSlotsByName(Dialog_Choose_Scale_Type)

        self.btn_sm110.clicked.connect(self.on_btn_sm110)
        self.btn_sm120.clicked.connect(self.on_btn_sm120)


    def retranslateUi(self, Dialog_Choose_Scale_Type):
        Dialog_Choose_Scale_Type.setWindowTitle(_translate("Dialog_Choose_Scale_Type", "Select Scale Type", None))
        self.btn_sm110.setText(_translate("Dialog_Choose_Scale_Type", "SM-110", None))
        self.btn_sm120.setText(_translate("Dialog_Choose_Scale_Type", "SM-120", None))


if __name__ == "__main__":
    import sys

    common.log_init()
    app = QtGui.QApplication(sys.argv)
    Dialog_Choose_Scale_Type = QtGui.QDialog()
    ui = Ui_Dialog_Choose_Scale_Type()
    ui.setupUi(Dialog_Choose_Scale_Type)
    Dialog_Choose_Scale_Type.show()
    sys.exit(app.exec_())

