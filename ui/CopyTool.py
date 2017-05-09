# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CopyTool.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import re
import os
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from Ip4 import Ip4Edit

sys.path.append('.')
sys.path.append('..')

import libsm110.easy

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


class ScaleIPDelegate(QItemDelegate):
    # def __init__(self, comboModel, parent=None):
    def __init__(self, parent=None):
        #super(ScaleIPDelegate, self).__init__(parent)
        super(ScaleIPDelegate, self).__init__()
        self.parent = parent

    # def paint(self, painter, option, index):
    #     super(ScaleIPDelegate, self).paint(painter, option, index)
    #     # print "paint"
    #     pass

    def __createIpControl(self, parent):
        view = Ip4Edit(parent)
        return view

    def createEditor(self, parent, option, index):
        # return None
        # print "createEditor"
        return self.__createIpControl(parent)

    def setEditorData(self, editor, index):
        # print "setEditorData:", editor
        # super(ScaleIPDelegate, self).setEditorData(editor, index)
        str_data = index.model().data(index, Qt.EditRole).toString()
        editor.setText(str_data)

    def setModelData(self, editor, model, index):
        # print "setModelData:", editor.text()
        # print "row:", index.row()
        # realidx = editor.model().index(editor.currentIndex(), 0)  # 确保取第一列的值
        # value = editor.model().data(realidx)
        # print model.data(model.index(0, 1, QModelIndex())).toString()
        # model.setData(index, value, Qt.EditRole)
        pat = re.compile("(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})")
        m = pat.match(editor.text())
        if m:
            model.setData(index, editor.text())

            # print type(model)
            # print model.rowCount()
            # print index.row()

            if index.row() == model.rowCount()-1:
                # model.addRow('')
                # model.itemsAdded('')
                it = QtGui.QListWidgetItem('')
                it.setFlags(it.flags() | Qt.ItemIsEditable)
                # self.parent.addItem(it)
                model.appendRow(QStandardItem(''))
        elif editor.text():
            QtGui.QMessageBox.critical(
                None,
                _fromUtf8("错误"),
                _fromUtf8(u"不是有效的IP地址"))


class Ui_CopyToolDialog(object):

    def getfile(self):
        fname = QFileDialog.getOpenFileName(None, u'打开文件', '', "*.*(*.*)")
        return fname

    def savefile(self):
        fname = QFileDialog.getSaveFileName(None, u'保存文件', '', "*.*(*.*)")
        return fname

    def start_do_copy(self):
        file_data = ""
        map_table = {
            u"标签格式": "Prf",
            u"商品信息": "Plu",
            u"文本信息": "Tex",
        }

        cur_item_text = unicode(self.lv_scalefile.currentItem().text())
        scale_file = map_table.get(cur_item_text, "Prf")

        if self.rb_source_fromfile.isChecked():
            file_path = unicode(self.edt_source_file.text())
            if os.path.exists(file_path):
                with open(file_path) as fp1:
                    file_data = fp1.read()
        elif self.rb_source_fromscale.isChecked():
            cur_scale = unicode(self.edt_source_scale.text())
            ease = libsm110.easy.Easy(cur_scale)

            # ease.easyReceiveFile(self.lv_scalefile.currentItem().)
            # print self.lv_scalefile.currentItem().text()
            temp_file_name = "temp1_" + cur_scale + "_" + scale_file + "_.dat"
            result = ease.easyReceiveFile(scale_file, temp_file_name)
            if result:
                with open(temp_file_name, 'r') as fp:
                    file_data = fp.read()
                os.remove(temp_file_name)
            # print result, file_data

        if file_data:
            if self.rb_target_fromfile.isChecked() and self.edt_target_file.text():
                with open(unicode(self.edt_target_file.text()), 'w') as fp:
                    fp.write(file_data)

                QtGui.QMessageBox.information(None, _fromUtf8("成功"), _fromUtf8(u"保存%s成功"%cur_item_text))

            elif self.rb_target_fromscale.isChecked():
                lst_scale = []
                # for i in range(self.lv_target_scale.count()):
                for i in range(self.lv_target_scale.model().rowCount()):
                    # lst_scale.append(unicode(self.lv_target_scale.item(i).text()))
                    # cur_scale = unicode(self.lv_target_scale.item(i).text())
                    cur_scale = unicode(self.lv_target_scale.model().item(i).text())
                    if not cur_scale:
                        continue
                    ease = libsm110.easy.Easy(cur_scale)
                    # temp_file_name = "temp2_" + scale_file + ".dat"
                    temp_file_name = "temp2_" + cur_scale + "_" + scale_file + "_" + ".dat"

                    with open(temp_file_name, 'w') as fp2:
                        fp2.write(file_data)
                    if ease.easySendFile(scale_file, temp_file_name):
                        QtGui.QMessageBox.information(
                            None,
                            _fromUtf8("成功"),
                            _fromUtf8(u"发送%s到%s成功" % (cur_item_text, cur_scale)))
                    else:
                        QtGui.QMessageBox.critical(
                            None,
                            _fromUtf8("失败"),
                            _fromUtf8(u"发送%s到%s失败" % (cur_item_text, cur_scale)))

                    os.remove(temp_file_name)
        else:
            QtGui.QMessageBox.critical(None, _fromUtf8("失败"), _fromUtf8("来源是不正确的数据"))

    def check_radio_status(self):
        if self.rb_source_fromfile.isChecked():
            self.edt_source_file.setEnabled(True)
            self.edt_source_scale.setEnabled(False)
            self.btn_select_source_file.setEnabled(True)
        else:
            self.btn_select_source_file.setEnabled(False)
            self.edt_source_file.setEnabled(False)
            self.edt_source_scale.setEnabled(True)

        if self.rb_target_fromfile.isChecked():
            self.edt_target_file.setEnabled(True)
            self.lv_target_scale.setEnabled(False)
            self.btn_select_target_file.setEnabled(True)
        else:
            self.btn_select_target_file.setEnabled(False)
            self.edt_target_file.setEnabled(False)
            self.lv_target_scale.setEnabled(True)

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(678, 391)
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(210, 15, 421, 106))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.rb_source_fromfile = QtGui.QRadioButton(self.groupBox)
        self.rb_source_fromfile.setGeometry(QtCore.QRect(15, 30, 70, 16))
        self.rb_source_fromfile.setChecked(True)
        self.rb_source_fromfile.setObjectName(_fromUtf8("rb_source_fromfile"))
        self.rb_source_fromscale = QtGui.QRadioButton(self.groupBox)
        self.rb_source_fromscale.setGeometry(QtCore.QRect(15, 60, 89, 16))
        self.rb_source_fromscale.setChecked(False)
        self.rb_source_fromscale.setObjectName(_fromUtf8("rb_source_fromscale"))
        self.edt_source_file = QtGui.QLineEdit(self.groupBox)
        self.edt_source_file.setGeometry(QtCore.QRect(90, 30, 256, 20))
        self.edt_source_file.setObjectName(_fromUtf8("edt_source_file"))
        # self.edt_source_scale = QtGui.QLineEdit(self.groupBox)
        self.edt_source_scale = Ip4Edit(self.groupBox)
        self.edt_source_scale.setGeometry(QtCore.QRect(90, 60, 200, 20))
        self.edt_source_scale.setObjectName(_fromUtf8("edt_source_scale"))
        self.btn_select_source_file = QtGui.QPushButton(self.groupBox)
        self.btn_select_source_file.setGeometry(QtCore.QRect(360, 30, 46, 20))
        self.btn_select_source_file.setObjectName(_fromUtf8("btn_select_source_file"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(210, 150, 421, 196))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.rb_target_fromfile = QtGui.QRadioButton(self.groupBox_2)
        self.rb_target_fromfile.setGeometry(QtCore.QRect(15, 30, 70, 16))
        self.rb_target_fromfile.setChecked(True)
        self.rb_target_fromfile.setObjectName(_fromUtf8("rb_source_fromfile_2"))
        self.rb_target_fromscale = QtGui.QRadioButton(self.groupBox_2)
        self.rb_target_fromscale.setGeometry(QtCore.QRect(15, 60, 89, 16))
        self.rb_target_fromscale.setObjectName(_fromUtf8("rb_source_fromscale_2"))
        self.edt_target_file = QtGui.QLineEdit(self.groupBox_2)
        self.edt_target_file.setGeometry(QtCore.QRect(90, 30, 256, 20))
        self.edt_target_file.setObjectName(_fromUtf8("edt_target_file"))
        self.lv_target_scale = QtGui.QListView(self.groupBox_2)
        # self.lv_target_scale = QtGui.QListWidget(self.groupBox_2)
        self.lv_target_scale.setGeometry(QtCore.QRect(90, 60, 256, 106))
        self.lv_target_scale.setObjectName(_fromUtf8("lv_target_scale"))
        self.btn_select_target_file = QtGui.QPushButton(self.groupBox_2)
        self.btn_select_target_file.setGeometry(QtCore.QRect(360, 30, 46, 20))
        self.btn_select_target_file.setObjectName(_fromUtf8("btn_select_target_file"))
        self.lv_scalefile = QtGui.QListWidget(Dialog)
        self.lv_scalefile.setGeometry(QtCore.QRect(15, 45, 166, 256))
        self.lv_scalefile.setObjectName(_fromUtf8("lv_scalefile"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15, 15, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btn_start = QtGui.QPushButton(Dialog)
        self.btn_start.setGeometry(QtCore.QRect(15, 315, 166, 31))
        self.btn_start.setObjectName(_fromUtf8("btn_start"))

        model = QStandardItemModel(self.lv_target_scale)
        item = QStandardItem('')
        # item.setCheckable(True)
        model.appendRow(item)
        self.lv_target_scale.setModel(model)

        self.lv_target_scale.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.lv_target_scale.setItemDelegate(ScaleIPDelegate(self.lv_target_scale))
        # self.lv_target_scale.setItemDelegateForColumn(0, ScaleIPDelegate(self.lv_target_scale))
        # self.lv_target_scale.setViewMode(QListView.ListMode)

        # it = QtGui.QListWidgetItem('', self.lv_target_scale)
        # self.lv_target_scale.setSelectionMode(QAbstractItemView.SingleSelection)
        # it.setFlags(it.flags() | Qt.ItemIsEditable)
        # self.lv_target_scale.addItem(it)

        # self.edt_source_scale.setText(QString("192.168.68.122"))

        self.check_radio_status()
        self.rb_source_fromfile.toggled.connect(lambda x: self.check_radio_status())
        self.rb_source_fromscale.toggled.connect(lambda x: self.check_radio_status())
        self.rb_target_fromfile.toggled.connect(lambda x: self.check_radio_status())
        self.rb_target_fromscale.toggled.connect(lambda x: self.check_radio_status())

        self.btn_select_source_file.clicked.connect(lambda: self.edt_source_file.setText(self.getfile()))
        self.btn_select_target_file.clicked.connect(lambda: self.edt_target_file.setText(self.savefile()))

        self.btn_start.clicked.connect(self.start_do_copy)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "寺冈秤复制工具", None))
        self.groupBox.setTitle(_translate("Dialog", "来源", None))
        self.rb_source_fromfile.setText(_translate("Dialog", "数据文件", None))
        self.rb_source_fromscale.setText(_translate("Dialog", "秤", None))
        self.btn_select_source_file.setText(_translate("Dialog", "...", None))
        self.groupBox_2.setTitle(_translate("Dialog", "目的", None))
        self.rb_target_fromfile.setText(_translate("Dialog", "数据文件", None))
        self.rb_target_fromscale.setText(_translate("Dialog", "秤", None))
        self.btn_select_target_file.setText(_translate("Dialog", "...", None))
        self.label.setText(_translate("Dialog", "【秤文件】", None))
        self.btn_start.setText(_translate("Dialog", "开始", None))

        self.lv_scalefile.addItem(u'标签格式')
        self.lv_scalefile.addItem(u'商品信息')
        self.lv_scalefile.addItem(u'文本信息')

        self.lv_scalefile.setCurrentRow(0)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    # Dialog = MyDialog()
    ui = Ui_CopyToolDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

