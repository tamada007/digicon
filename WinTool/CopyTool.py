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
from Ip4 import Ip4Edit, MyDialog, MyFont, resource_path

sys.path.append('.')
sys.path.append('..')

import libsm110.easy
import libsm120.easy

from common import common

g_scale_file_table_sm110 = {
    'Prf': u'标签格式',
    'Plu': u'商品信息',
    'Tex': u'文本信息',
    'Flb': u'自定义条码',
    'Kas': u'预置键',
    'Ima': u'图片',
    'Tbt': u'二维码',
    'Spe': u'Specs',
}

g_scale_file_table_sm120 = {
    'Prf': u'标签格式头',
    'Pff': u'标签格式明细',
    'Plu': u'商品信息',
    'Spm': u'特殊信息',
    'Ing': u'成份',
    'Tex': u'文本信息',
    'Flb': u'自定义条码',
    'Kas': u'预置键',
    'Ima': u'图片',
    'Tbt': u'二维码',
    'Spe': u'Specs',
}

g_scale_sm120_delete_flag = {
    'Prf': True,
    'Pff': True,
    'Plu': True,
    'Spm': True,
    'Ing': True,
    'Tex': True,
    'Flb': True,
    'Kas': True,
    'Ima': True,
    'Tbt': True,
    'Spe': False,
}

g_delete_flag_asked = False
g_delete_flag = False


g_scale_file_table = {}

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


class MyListView(QtGui.QListView):
    def __init__(self, parent):
        super(MyListView, self).__init__(parent)
        # self.setContextMenuPolicy(Qt.ActionsContextMenu)

    def _remove(self):
        model = self.model()
        # print self.selectedIndexes()
        selected_row = self.selectedIndexes()[0]
        # print "row:", selected_row.row()
        if selected_row.row() != model.rowCount()-1:
            model.removeRow(selected_row.row())

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu()
        index = self.indexAt(event.pos())
        # print index.row()
        removeAction = QtGui.QAction(u'删除', self)
        removeAction.triggered.connect(self._remove)
        self.menu.addAction(removeAction)
        self.menu.popup(QtGui.QCursor.pos())


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
                item = QStandardItem('')
                font = QtGui.QFont()
                font.setFamily(_fromUtf8("Arial"))
                font.setPointSize(14)
                item.setFont(font)
                # model.appendRow(QStandardItem(''))
                model.appendRow(item)
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

        global g_scale_file_table

        file_data = ""
        file_list = []

        # scale_file = unicode(self.lv_scalefile.currentItem().data(1).toString())
        # cur_item_text = unicode(self.lv_scalefile.currentItem().data(0).toString())

        # cur_item_text = unicode(self.lv_scalefile.currentItem().text())
        # scale_file = map_table.get(cur_item_text, "Prf")

        cur_item_text = ""
        cur_item_list = []

        if self.rb_source_fromfile.isChecked():
            file_path = unicode(self.edt_source_file.text())
            if os.path.exists(file_path):
                with open(file_path) as fp1:
                    file_data = fp1.read()
        elif self.rb_source_fromscale.isChecked():
            cur_scale = unicode(self.edt_source_scale.text())
            if self.main_dialog.getParams()["scaleType"] == "sm110":
                ease = libsm110.easy.Easy(cur_scale)
            else:
                ease = libsm120.easy.Easy(cur_scale)

            # ease.easyReceiveFile(self.lv_scalefile.currentItem().)
            # print self.lv_scalefile.currentItem().text()

            for selected_item in self.lv_scalefile.selectedItems():
                selected_scale_file = unicode(selected_item.data(1).toString())
                cur_item_list.append(g_scale_file_table.get(selected_scale_file))

                # cur_item_text = unicode(selected_item.data(0).toString())
                temp_file_name = "temp1_" + cur_scale + "_" + selected_scale_file + "_.dat"
                result = ease.easyReceiveFile(selected_scale_file, temp_file_name)
                if result:
                    temp_file_data = ""
                    with open(temp_file_name, 'r') as fp:
                        temp_file_data = fp.read()
                    os.remove(temp_file_name)

                    try:
                        for line_data in temp_file_data.split("\n"):
                            if line_data.strip(' \r'):
                                file_list.append(selected_scale_file + ":" + line_data.rstrip(" \r"))
                    except Exception, ex:
                        common.log_err(ex)


            # temp_file_name = "temp1_" + cur_scale + "_" + scale_file + "_.dat"
            # result = ease.easyReceiveFile(scale_file, temp_file_name)
            # if result:
            #     with open(temp_file_name, 'r') as fp:
            #         file_data = fp.read()
            #     os.remove(temp_file_name)
            file_data = "\n".join(file_list)

        cur_item_text = ",".join(cur_item_list)

        if file_data:
            if self.rb_target_fromfile.isChecked() and self.edt_target_file.text():
                with open(unicode(self.edt_target_file.text()), 'w') as fp:
                    fp.write(file_data)

                QtGui.QMessageBox.information(None, _fromUtf8("成功"), _fromUtf8(u"保存%s成功"%cur_item_text))

            elif self.rb_target_fromscale.isChecked():
                lst_scale = []
                # for i in range(self.lv_target_scale.count()):
                dict_data = {}
                for line_data in file_data.split("\n"):
                    line_data = line_data.rstrip(" \r")
                    pat = re.compile("(\w+):(.+)")
                    m = pat.match(line_data)
                    if m:
                        if not m.group(1) in dict_data:
                            dict_data[m.group(1)] = ""
                        dict_data[m.group(1)] += m.group(2) + "\n"

                for i in range(self.lv_target_scale.model().rowCount()):
                    # lst_scale.append(unicode(self.lv_target_scale.item(i).text()))
                    # cur_scale = unicode(self.lv_target_scale.item(i).text())
                    cur_scale = unicode(self.lv_target_scale.model().item(i).text())
                    if not cur_scale:
                        continue
                    if self.main_dialog.getParams()["scaleType"] == "sm110":
                        ease = libsm110.easy.Easy(cur_scale)
                    else:
                        ease = libsm120.easy.Easy(cur_scale)
                    cur_item_list_succeed = []
                    cur_item_list_failed = []
                    for scale_file, scale_file_data in dict_data.items():

                        temp_file_name = "temp2_" + cur_scale + "_" + scale_file + "_" + ".dat"

                        cur_item_text = g_scale_file_table.get(scale_file)

                        global g_delete_flag
                        global g_delete_flag_asked

                        # sm120时，询问是否清除之前的记录
                        if self.getCurrentScaleType() == "sm120":
                            # 没有询问过时出框询问
                            if not g_delete_flag_asked:
                                g_delete_flag_asked = True
                                msgBox = QtGui.QMessageBox()
                                msgBox.setWindowTitle(_fromUtf8("询问"))
                                # msgBox.setText(_fromUtf8("询问"))
                                msgBox.setInformativeText(_fromUtf8("是否清除秤上的记录再发送?"))
                                msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
                                msgBox.setDefaultButton(QtGui.QMessageBox.Yes)
                                ret = msgBox.exec_()

                                if ret == QtGui.QMessageBox.Yes:
                                    g_delete_flag = True

                            if g_delete_flag and g_scale_sm120_delete_flag.get(scale_file):
                                common.log_info("clearing %s on %s" % (scale_file, cur_scale))
                                if not ease.easyDeleteFile(scale_file):
                                    QtGui.QMessageBox.critical(
                                        None,
                                        _fromUtf8("失败"),
                                        _fromUtf8(u"清除%s到%s失败" % (cur_item_text, cur_scale)))

                        with open(temp_file_name, 'w') as fp2:
                            fp2.write(scale_file_data)
                        if ease.easySendFile(scale_file, temp_file_name):
                            cur_item_list_succeed.append(cur_item_text)
                            # QtGui.QMessageBox.information(
                            #     None,
                            #     _fromUtf8("成功"),
                            #     _fromUtf8(u"发送%s到%s成功" % (cur_item_text, cur_scale)))
                        else:
                            cur_item_list_failed.append(cur_item_text)
                            # QtGui.QMessageBox.critical(
                            #     None,
                            #     _fromUtf8("失败"),
                            #     _fromUtf8(u"发送%s到%s失败" % (cur_item_text, cur_scale)))

                        os.remove(temp_file_name)

                    if len(cur_item_list_succeed) > 0:
                        QtGui.QMessageBox.information(
                            None,
                            _fromUtf8("成功"),
                            _fromUtf8(u"发送%s到%s成功" % (",".join(cur_item_list_succeed), cur_scale)))

                    if len(cur_item_list_failed) > 0:
                        QtGui.QMessageBox.critical(
                            None,
                            _fromUtf8("失败"),
                            _fromUtf8(u"发送%s到%s失败" % (",".join(cur_item_list_failed), cur_scale)))

        else:
            QtGui.QMessageBox.critical(None, _fromUtf8("失败"), _fromUtf8("来源是不正确的数据"))

    def check_radio_status(self):
        if self.rb_source_fromfile.isChecked():
            self.edt_source_file.setEnabled(True)
            self.edt_source_scale.setEnabled(False)
            self.btn_select_source_file.setEnabled(True)
            self.lv_scalefile.setEnabled(False)
        else:
            self.btn_select_source_file.setEnabled(False)
            self.edt_source_file.setEnabled(False)
            self.edt_source_scale.setEnabled(True)
            self.lv_scalefile.setEnabled(True)

        if self.rb_target_fromfile.isChecked():
            self.edt_target_file.setEnabled(True)
            self.lv_target_scale.setEnabled(False)
            self.btn_select_target_file.setEnabled(True)
        else:
            self.btn_select_target_file.setEnabled(False)
            self.edt_target_file.setEnabled(False)
            self.lv_target_scale.setEnabled(True)

    def getCurrentScaleType(self):
        return self.main_dialog.getParams()["scaleType"]

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(678, 391)
        Dialog.setWindowModality(QtCore.Qt.WindowModal)

        self.main_dialog = Dialog
        global g_scale_file_table

        # if self.main_dialog.getParams()["scaleType"] == "sm110" \
        g_scale_file_table = \
            g_scale_file_table_sm110 \
                if self.getCurrentScaleType() == "sm110" \
                else g_scale_file_table_sm120

        icon_file_path = resource_path("as.png")
        icon = QtGui.QIcon(icon_file_path)
        # icon.addPixmap(QtGui.QPixmap(_fromUtf8(resource_path("as.ico"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)


        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setFont(MyFont(10))
        self.groupBox.setGeometry(QtCore.QRect(210, 15, 421, 106))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.rb_source_fromfile = QtGui.QRadioButton(self.groupBox)
        self.rb_source_fromfile.setFont(MyFont(10))
        self.rb_source_fromfile.setGeometry(QtCore.QRect(15, 30, 70, 16))
        self.rb_source_fromfile.setChecked(True)
        self.rb_source_fromfile.setObjectName(_fromUtf8("rb_source_fromfile"))
        self.rb_source_fromscale = QtGui.QRadioButton(self.groupBox)
        self.rb_source_fromscale.setFont(MyFont(10))
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
        self.groupBox_2.setFont(MyFont(10))
        self.groupBox_2.setGeometry(QtCore.QRect(210, 150, 421, 196))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.rb_target_fromfile = QtGui.QRadioButton(self.groupBox_2)
        self.rb_target_fromfile.setFont(MyFont(10))
        self.rb_target_fromfile.setGeometry(QtCore.QRect(15, 30, 70, 16))
        self.rb_target_fromfile.setChecked(True)
        self.rb_target_fromfile.setObjectName(_fromUtf8("rb_source_fromfile_2"))
        self.rb_target_fromscale = QtGui.QRadioButton(self.groupBox_2)
        self.rb_target_fromscale.setFont(MyFont(10))
        self.rb_target_fromscale.setGeometry(QtCore.QRect(15, 60, 89, 16))
        self.rb_target_fromscale.setObjectName(_fromUtf8("rb_source_fromscale_2"))
        self.edt_target_file = QtGui.QLineEdit(self.groupBox_2)
        self.edt_target_file.setGeometry(QtCore.QRect(90, 30, 256, 20))
        self.edt_target_file.setObjectName(_fromUtf8("edt_target_file"))
        # self.lv_target_scale = QtGui.QListView(self.groupBox_2)
        self.lv_target_scale = MyListView(self.groupBox_2)
        # self.lv_target_scale = QtGui.QListWidget(self.groupBox_2)
        self.lv_target_scale.setGeometry(QtCore.QRect(90, 60, 256, 106))
        self.lv_target_scale.setObjectName(_fromUtf8("lv_target_scale"))
        self.btn_select_target_file = QtGui.QPushButton(self.groupBox_2)
        self.btn_select_target_file.setGeometry(QtCore.QRect(360, 30, 46, 20))
        self.btn_select_target_file.setObjectName(_fromUtf8("btn_select_target_file"))
        self.lv_scalefile = QtGui.QListWidget(Dialog)
        self.lv_scalefile.setGeometry(QtCore.QRect(15, 45, 166, 256))
        self.lv_scalefile.setObjectName(_fromUtf8("lv_scalefile"))
        self.lv_scalefile.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.label = QtGui.QLabel(Dialog)
        self.label.setFont(MyFont(10))
        self.label.setGeometry(QtCore.QRect(15, 15, 101, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btn_start = QtGui.QPushButton(Dialog)
        self.btn_start.setFont(MyFont(10))
        self.btn_start.setGeometry(QtCore.QRect(15, 315, 166, 31))
        self.btn_start.setObjectName(_fromUtf8("btn_start"))

        model = QStandardItemModel(self.lv_target_scale)
        item = QStandardItem('')
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(14)
        item.setFont(font)


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

        from TimerMessageBox import TimerMessageBox
        messagebox = TimerMessageBox(1, Dialog, userMessage="当前秤型号为: " + Dialog.getParams()["scaleType"])
        messagebox.exec_()


    def retranslateUi(self, Dialog):
        # Dialog.setWindowTitle(_translate("Dialog", "寺冈秤复制工具", None))
        Dialog.setWindowTitle(_translate("Dialog", "寺冈秤复制工具 - " + self.main_dialog.getParams()["scaleType"], None))


        self.groupBox.setTitle(_translate("Dialog", "来源", None))
        self.rb_source_fromfile.setText(_translate("Dialog", "数据文件", None))
        self.rb_source_fromscale.setText(_translate("Dialog", "秤", None))
        self.btn_select_source_file.setText(_translate("Dialog", "...", None))
        self.groupBox_2.setTitle(_translate("Dialog", "目的", None))
        self.rb_target_fromfile.setText(_translate("Dialog", "数据文件", None))
        self.rb_target_fromscale.setText(_translate("Dialog", "秤", None))
        self.btn_select_target_file.setText(_translate("Dialog", "...", None))
        self.label.setText(_translate("Dialog", "【来源秤文件】", None))
        self.btn_start.setText(_translate("Dialog", "开始", None))

        # self.lv_scalefile.addItem(u'标签格式')
        # self.lv_scalefile.addItem(u'商品信息')
        # self.lv_scalefile.addItem(u'文本信息')
        # item1 = QListWidgetItem(u'标签格式')
        # item1.setData(1, 'Prf')
        # self.lv_scalefile.addItem(item1)
        # item1 = QListWidgetItem(u'商品信息')
        # item1.setData(1, 'Plu')
        # self.lv_scalefile.addItem(item1)
        # item1 = QListWidgetItem(u'文本信息')
        # item1.setData(1, 'Tex')
        # self.lv_scalefile.addItem(item1)
        # item1 = QListWidgetItem(u'自定义条码')
        # item1.setData(1, 'Flb')
        # self.lv_scalefile.addItem(item1)
        # item1 = QListWidgetItem(u'预置键')
        # item1.setData(1, 'Kas')
        # self.lv_scalefile.addItem(item1)

        global g_scale_file_table
        for k, v in g_scale_file_table.items():
            item1 = QListWidgetItem(v)
            item1.setData(1, k)
            self.lv_scalefile.addItem(item1)

        # self.lv_scalefile.setCurrentRow(0)


if __name__ == "__main__":
    import sys
    # import icon_rc
    # icon_rc.qInitResources()
    app = QtGui.QApplication(sys.argv)
    Dialog = MyDialog()
    ui = Ui_CopyToolDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

