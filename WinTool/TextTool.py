# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestTool_Prot.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import re
import os
import sys

sys.path.append('.')
sys.path.append('..')

# 默认为gbk,在encode.txt可设置编码
current_encoding = 'gbk'
if os.path.isfile('encode.txt'):
    with open('encode.txt') as fp:
        current_encoding = fp.readline().strip()

sys.getdefaultencoding()
reload(sys)
# sys.setdefaultencoding("utf-8")
sys.setdefaultencoding(current_encoding)  # @UndefinedVariable


from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from Ip4 import Ip4Edit, MyDialog, MyFont, resource_path

from common.converter import ScalesConverter
from common import common, converter

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

font_map = {
    "S1": 0,
    "S2": 1,
    "S3": 2,
    "S4": 3,
    "S5": 4,
    "S6": 0xE,
    "G1": 0x16,
    "G2": 0x17,
    "G3": 0x14,
    "G4": 0x15,
    "G5": 0x18,
    "G6": 0x19,
}

class ScaleItemString(object):
    # def __init__(self, scale_ip, scale_no, store_no, store_name):
    #     self.scale_ip = scale_ip
    #     self.scale_no = scale_no
    #     self.store_no = store_no
    #     self.store_name = store_name
    def __init__(self, **kargs):
        # print kargs
        self.scale_ip = kargs.get("scale_ip")
        self.scale_no = kargs.get("scale_no")
        self.store_no = kargs.get("store_no")
        self.store_name = kargs.get("store_name")
        self.other = kargs.get("other")
        self.font_scale_no = kargs.get("font_scale_no")
        self.font_store_no = kargs.get("font_store_no")
        self.font_store_name = kargs.get("font_store_name")
        self.font_other = kargs.get("font_other")

    def __str__(self):
        return self.scale_ip + "," + self.store_no


class ToolsView(QtGui.QTableView):
    def __init__(self, parent=None):
        super(ToolsView, self).__init__(parent)
        # self.setSortingEnabled(True)
        # self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

    def clear(self):
        # for row in range(self.model().rowCount()):
        for row in reversed(range(self.model().rowCount())):
            self.model().removeRow(row)

        self.model().appendRow('')

    def remove(self):
        # print self.model().data(self.model().index(0, 0)).toString()
        rows = self.selectionModel().selectedRows(0)
        for r in reversed(rows):
            # print r.row()
            if self.model().data(self.model().index(r.row(), 0)).toString():
                self.model().removeRow(r.row())
                # self.model().removeRow()

    def contextMenuEvent(self, event):
        self.menu = QtGui.QMenu()
        index = self.indexAt(event.pos())
        # print index.row()
        removeAction = QtGui.QAction(u'删除', self)
        removeAction.triggered.connect(self.remove)
        renameAllAction = QtGui.QAction(u'清空', self)
        renameAllAction.triggered.connect(self.clear)
        self.menu.addAction(removeAction)
        self.menu.addAction(renameAllAction)
        self.menu.popup(QtGui.QCursor.pos())

    # def mousePressEvent(self, event):
    #     mouseBtn = event.button()
    #     if mouseBtn == Qt.RightButton:
    #         rows = self.selectionModel().selectedRows(0)
    #         # for r in rows:
    #         #     print r.row()
    #     super(ToolsView, self).mousePressEvent(event)


class ScaleIPDelegate(QItemDelegate):
    # def __init__(self, comboModel, parent=None):
    def __init__(self, parent=None):
        #super(ScaleIPDelegate, self).__init__(parent)
        super(ScaleIPDelegate, self).__init__()
        self.parent = parent

    def __createIpControl(self, parent):
        view = Ip4Edit(parent)
        return view

    def createEditor(self, parent, option, index):
        return self.__createIpControl(parent)

    def setEditorData(self, editor, index):
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
            scale_no = m.group(4)
            # self.edt_scaleno.setText(scale_no)
            model.setData(model.index(index.row(), 1), QVariant(scale_no))

            model.setData(model.index(index.row(), 3), self.parent.edt_storeno.text())
            model.setData(model.index(index.row(), 5), self.parent.edt_storename.text())
            model.setData(model.index(index.row(), 7), self.parent.edt_other.text())

            model.setData(model.index(index.row(), 2), self.parent.comboBox.currentText())
            model.setData(model.index(index.row(), 4), self.parent.comboBox_2.currentText())
            model.setData(model.index(index.row(), 6), self.parent.comboBox_3.currentText())
            model.setData(model.index(index.row(), 8), self.parent.comboBox_4.currentText())

            if index.row() == model.rowCount()-1:
                model.appendRow('')


class FontDelegate(QItemDelegate):
    def __init__(self, comboModel, parent=None):
        QItemDelegate.__init__(self, parent)
        self.comboModel = comboModel

    def __createComboView(self, parent):
        view = QtGui.QTableView(parent)
        view.setModel(self.comboModel)
        view.setAutoScroll(False)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.resizeColumnsToContents()
        view.resizeRowsToContents()
        view.setMinimumWidth(view.horizontalHeader().length())
        return view

    def createEditor(self, parent, option, index):
        combo = QtGui.QComboBox(parent)
        # !! The important part: First set the model, then the view on the combo box
        combo.setModel(self.comboModel)
        # combo.setModelColumn(1)
        combo.setView(self.__createComboView(parent))
        return combo

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole).toString()
        editor.setCurrentIndex(editor.findText(value))

    def setModelData(self, editor, model, index):
        if editor.currentIndex() >= 0:
            realidx = editor.model().index(editor.currentIndex(), 0)  # 确保取第一列的值
            value = editor.model().data(realidx)
            print model.data(model.index(0, 1, QModelIndex())).toString()
            model.setData(index, value, Qt.EditRole)


class Ui_TextToolDialog(object):

    # def on_btn_add(self):
    #     pat = re.compile("(\d{,3})\.(\d{,3})\.(\d{,3})\.(\d{,3})")
    #     m = pat.match(self.edt_scale.text())
    #     if m:
    #         # model = self.tbl_scale.selectionModel()
    #         model = self.tbl_scale.model()
    #         model.appendRow([
    #             QStandardItem(self.edt_scale.text()),
    #             QStandardItem(self.edt_scaleno.text()),
    #             QStandardItem(self.edt_storeno.text()),
    #             QStandardItem(self.edt_storename.text()),
    #             QStandardItem(self.edt_other.text())])
    #
    #         model.setData(model.index(model.rowCount()-1, 5, QModelIndex()), QVariant(ScaleItemString(
    #                 scale_ip=unicode(self.edt_scale.text()).encode('gbk'),
    #                 scale_no=unicode(self.edt_scaleno.text()).encode('gbk'),
    #                 store_no=unicode(self.edt_storeno.text()).encode('gbk'),
    #                 store_name=unicode(self.edt_storename.text()).encode('gbk'),
    #                 other=unicode(self.edt_other.text()).encode('gbk')
    #             )))
    #
    #         # item = QtGui.QListWidgetItem("%-16s%-10s%-10s%-10s%-10s" % (
    #         #     self.edt_scale.text(),
    #         #     self.edt_scaleno.text(),
    #         #     self.edt_storeno.text(),
    #         #     self.edt_storename.text(),
    #         #     self.edt_other.text()
    #         # ))
    #         # indx = self.lst_scale.count()
    #         # item.setData(Qt.UserRole, ScaleItemString(
    #         #         scale_ip=unicode(self.edt_scale.text()).encode('gbk'),
    #         #         scale_no=unicode(self.edt_scaleno.text()).encode('gbk'),
    #         #         store_no=unicode(self.edt_storeno.text()).encode('gbk'),
    #         #         store_name=unicode(self.edt_storename.text()).encode('gbk'),
    #         #         other=unicode(self.edt_other.text()).encode('gbk')
    #         # ))
    #         # self.lst_scale.addItem(item)
    #         # self.lst_scale.setCurrentRow(0)
    #
    #         # self.lst_scale.addItem(self.edt_scale.text())
    #         self.edt_scale.setText('')
    #         self.edt_scaleno.setText('')
    #     else:
    #         QtGui.QMessageBox.critical(None, _fromUtf8("错误"), _fromUtf8("IP地址不合法"))
    #
    # def on_btn_remove(self):
    #     # item = self.lst_scale.takeItem(self.lst_scale.currentRow())
    #     # item = None
    #
    #     indexes = self.tbl_scale.selectionModel().selectedRows()
    #     for index in sorted(indexes):
    #         self.tbl_scale.model().removeRow(index.row())
    #
    # def on_btn_clear(self):
    #     # indexes = self.tbl_scale.selectionModel().selectedRows()
    #     # for index in sorted(indexes):
    #     #     print('Row %d is selected' % index.row())
    #     # self.lst_scale.clear()
    #
    #     # self.tbl_scale.model().clear()
    #     model = self.tbl_scale.model()
    #     for i in range(model.rowCount()):
    #         model.removeRow(i)
    #     # qitems = self.lst_scale.selectedItems()
    #     # for i in qitems:
    #     #     j = QtGui.QListWidgetItem(i)
    #     #     print unicode(j.data(Qt.UserRole).toPyObject().store_name)

    def create_json(self, file_name):
        str = """[
            { "source_expr": "$(1)", "target_field": "TextCode" },
            { "source_expr": "$(2)", "target_field": "Text" },
            { "source_expr": "$(3)", "target_field": "TextFont" }
        ]"""
        with open(file_name, "w") as fp1:
            fp1.write(str)

    def create_text(self, scale_data_item):
        str_data = "1,%s,%s\r\n2,%s,%s\r\n3,%s,%s\r\n4,%s,%s" % (
            scale_data_item.scale_no,
            str(font_map.get(scale_data_item.font_scale_no, 0)),
            scale_data_item.store_no,
            str(font_map.get(scale_data_item.font_store_no, 0)),
            scale_data_item.store_name,
            str(font_map.get(scale_data_item.font_store_name, 0)),
            scale_data_item.other,
            str(font_map.get(scale_data_item.font_other, 0)),
        )
        file_name_created = "%s.38.csv" % scale_data_item.scale_ip
        try:
            with open(file_name_created, "w") as fp1:
                # fp1.write(unicode(str_data).encode('gbk'))
                fp1.write(unicode(str_data).encode(sys.getdefaultencoding()))
        except Exception, ex:
            common.log_err(ex)
        return file_name_created

    def on_btn_send(self):
        # print "c p 1"

        self.btn_send.setEnabled(False)

        json_file = "scale_text.json"
        self.create_json(json_file)

        scale_success_list = []
        scale_failed_list = []

        lst_scale_infos = []
        model = self.tbl_scale.model()
        for row in range(model.rowCount() - 1):
            scale_ip = unicode(model.data(model.index(row, 0)).toPyObject())
            scale_no = unicode(model.data(model.index(row, 1)).toPyObject())
            store_no = unicode(model.data(model.index(row, 3)).toPyObject())
            store_name = unicode(model.data(model.index(row, 5)).toPyObject())
            other = unicode(model.data(model.index(row, 7)).toPyObject())

            font_scale_no = unicode(model.data(model.index(row, 2)).toPyObject())
            font_store_no = unicode(model.data(model.index(row, 4)).toPyObject())
            font_store_name = unicode(model.data(model.index(row, 6)).toPyObject())
            font_other = unicode(model.data(model.index(row, 8)).toPyObject())
            lst_scale_infos.append(ScaleItemString(
                scale_ip=scale_ip,
                scale_no=scale_no,
                store_no=store_no,
                store_name=store_name,
                other=other,
                font_scale_no=font_scale_no,
                font_store_no=font_store_no,
                font_store_name=font_store_name,
                font_other=font_other))

        scales_converter = ScalesConverter(converter.ConvertDesc_TEXT)
        model = self.tbl_scale.model()
        for cur_scale_info in lst_scale_infos:
            # print cur_i
            # print type(data), data
            csv_file = self.create_text(cur_scale_info)

            # print cur_scale_item.scale_ip
            if self.main_dialog.getParams()["scaleType"] == "sm110":
                result = scales_converter.easyImportMaster(cur_scale_info.scale_ip+":sm110", csv_file, json_file)
            else:
                result = scales_converter.easyImportMaster(cur_scale_info.scale_ip, csv_file, json_file)

            if result:
                scale_success_list.append(cur_scale_info.scale_ip)
            else:
                scale_failed_list.append(cur_scale_info.scale_ip)


        # scales_converter = ScalesConverter(converter.ConvertDesc_TEXT)
        # model = self.tbl_scale.model()
        # for cur_i in range(model.rowCount()):
        #     # print cur_i
        #     cur_scale_item = model.data(model.index(cur_i, 5, QModelIndex())).toPyObject()
        #     # print type(data), data
        #     csv_file = self.create_text(cur_scale_item)
        #
        #     # print cur_scale_item.scale_ip
        #     result = scales_converter.easyImportMaster(cur_scale_item.scale_ip+":sm110", csv_file, json_file)
        #
        #     if result:
        #         scale_success_list.append(cur_scale_item.scale_ip)
        #     else:
        #         scale_failed_list.append(cur_scale_item.scale_ip)

        # for cur_i in range(self.lst_scale.count()):
        #     cur_item = self.lst_scale.item(cur_i)
        #     cur_scale_item = cur_item.data(Qt.UserRole).toPyObject()
        #     csv_file = self.create_text(cur_scale_item)
        #
        #     scales_converter = ScalesConverter(converter.ConvertDesc_TEXT)
        #     # print cur_scale_item.scale_ip
        #     result = scales_converter.easyImportMaster(cur_scale_item.scale_ip+":sm110", csv_file, json_file)
        #
        #     if result:
        #         scale_success_list.append(cur_scale_item.scale_ip)
        #     else:
        #         scale_failed_list.append(cur_scale_item.scale_ip)

        if len(scale_failed_list) > 0:
            QtGui.QMessageBox.critical(None,
                _fromUtf8("错误"),
                _fromUtf8("以下秤发送文本失败:" + "\r\n".join(scale_failed_list)))
        else:
            QtGui.QMessageBox.information(None,
                _fromUtf8("成功"),
                _fromUtf8("文本信息已发送到所有秤"))

        self.btn_send.setEnabled(True)

        common.close_all_sqlite_db()
        # print cur_item.data(Qt.UserRole).toPyObject().scale_ip

    # def on_scale_changed(self, args, **kargs):
    #     # self.lst_scale.addItem()
    #     pat = re.compile("(\d{,3})\.(\d{,3})\.(\d{,3})\.(\d{,3})")
    #     m = pat.match(args)
    #     if m:
    #         scale_no = m.group(4)
    #         self.edt_scaleno.setText(scale_no)

    def setupUi(self, Dialog):

        # print Dialog.params["scaleType"]
        self.main_dialog = Dialog

        from TimerMessageBox import TimerMessageBox
        messagebox = TimerMessageBox(1, Dialog, userMessage="当前秤型号为: " + Dialog.getParams()["scaleType"])
        messagebox.exec_()


        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(639, 438)

        icon_file_path = resource_path("as.png")
        icon = QtGui.QIcon(icon_file_path)
        # icon.addPixmap(QtGui.QPixmap(_fromUtf8(resource_path("as.ico"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(15, 15, 63, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.btn_send = QtGui.QPushButton(Dialog)
        self.btn_send.setFont(MyFont(10))
        self.btn_send.setGeometry(QtCore.QRect(495, 345, 111, 41))
        self.btn_send.setObjectName(_fromUtf8("btn_send"))
        self.horizontalLayoutWidget = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(15, 225, 586, 46))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.edt_scaleno = QtGui.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edt_scaleno.sizePolicy().hasHeightForWidth())
        self.edt_scaleno.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.edt_scaleno.setFont(font)
        self.edt_scaleno.setObjectName(_fromUtf8("edt_scaleno"))
        self.horizontalLayout.addWidget(self.edt_scaleno)
        self.comboBox = QtGui.QComboBox(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setMinimumSize(QtCore.QSize(50, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_4 = QtGui.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.edt_storeno = QtGui.QLineEdit(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.edt_storeno.setFont(font)
        self.edt_storeno.setObjectName(_fromUtf8("edt_storeno"))
        self.horizontalLayout.addWidget(self.edt_storeno)
        self.comboBox_2 = QtGui.QComboBox(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy)
        self.comboBox_2.setMinimumSize(QtCore.QSize(50, 0))
        self.comboBox_2.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.comboBox_2.setFont(font)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_2)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(15, 285, 586, 46))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_8 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_3.addWidget(self.label_8)
        self.edt_storename = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.edt_storename.setFont(font)
        self.edt_storename.setObjectName(_fromUtf8("edt_storename"))
        self.horizontalLayout_3.addWidget(self.edt_storename)
        self.comboBox_3 = QtGui.QComboBox(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_3.sizePolicy().hasHeightForWidth())
        self.comboBox_3.setSizePolicy(sizePolicy)
        self.comboBox_3.setMinimumSize(QtCore.QSize(50, 0))
        self.comboBox_3.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.comboBox_3.setFont(font)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.comboBox_3)
        spacerItem1 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_9 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.edt_other = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.edt_other.setFont(font)
        self.edt_other.setObjectName(_fromUtf8("edt_other"))
        self.horizontalLayout_3.addWidget(self.edt_other)
        self.comboBox_4 = QtGui.QComboBox(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_4.sizePolicy().hasHeightForWidth())
        self.comboBox_4.setSizePolicy(sizePolicy)
        self.comboBox_4.setMinimumSize(QtCore.QSize(50, 0))
        self.comboBox_4.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.comboBox_4.setFont(font)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.comboBox_4)
        # self.tbl_scale = QtGui.QTableView(Dialog)
        self.tbl_scale = ToolsView(Dialog)
        self.tbl_scale.setGeometry(QtCore.QRect(15, 45, 586, 136))
        self.tbl_scale.setObjectName(_fromUtf8("tbl_scale"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(15, 195, 121, 24))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.edt_scaleno, self.edt_storeno)
        Dialog.setTabOrder(self.edt_storeno, self.edt_storename)
        Dialog.setTabOrder(self.edt_storename, self.edt_other)
        # self.btn_add.clicked.connect(self.on_btn_add)
        # self.btn_clear.clicked.connect(self.on_btn_clear)
        # self.edt_scale.textChanged.connect(self.on_scale_changed)
        self.btn_send.clicked.connect(self.on_btn_send)
        # self.btn_remove.clicked.connect(self.on_btn_remove)

        model = QStandardItemModel(1, 9, self.tbl_scale)
        model.setHorizontalHeaderLabels([
            # u'秤IP', u'秤号', u'店号', u'店名', u'其它', u'Hidden'
            u'秤IP', u'秤号', u'秤号字体', u'店号', u'店号字体', u'店名', u'店名字体', u'其它', u'其它字体'
        ])
        # model.setData(model.index(0, 0, QModelIndex()), QVariant(u'松鼠'))
        # model.setData(model.index(0, 1, QModelIndex()), QVariant(u'80cm'))
        # model.setData(model.index(0, 2, QModelIndex()), QVariant(u'12Kg'))
        self.tbl_scale.verticalHeader().setVisible(False)

        comboModel = QStandardItemModel(12, 2, self.tbl_scale)
        comboModel.setHorizontalHeaderLabels([u'字号', u'大小'])
        comboModel.setData(comboModel.index(0, 0), QVariant(u'S1'))
        comboModel.setData(comboModel.index(0, 1), QVariant(u'5x7'))
        comboModel.setData(comboModel.index(1, 0), QVariant(u'S2'))
        comboModel.setData(comboModel.index(1, 1), QVariant(u'6x10'))
        comboModel.setData(comboModel.index(2, 0), QVariant(u'S3'))
        comboModel.setData(comboModel.index(2, 1), QVariant(u'7x12'))
        comboModel.setData(comboModel.index(3, 0), QVariant(u'S4'))
        comboModel.setData(comboModel.index(3, 1), QVariant(u'7x16'))
        comboModel.setData(comboModel.index(4, 0), QVariant(u'S5'))
        comboModel.setData(comboModel.index(4, 1), QVariant(u'9x22'))
        comboModel.setData(comboModel.index(5, 0), QVariant(u'S6'))
        comboModel.setData(comboModel.index(5, 1), QVariant(u'22x40'))
        comboModel.setData(comboModel.index(6, 0), QVariant(u'G1'))
        comboModel.setData(comboModel.index(6, 1), QVariant(u'16x16'))
        comboModel.setData(comboModel.index(7, 0), QVariant(u'G2'))
        comboModel.setData(comboModel.index(7, 1), QVariant(u'32x32'))
        comboModel.setData(comboModel.index(8, 0), QVariant(u'G3'))
        comboModel.setData(comboModel.index(8, 1), QVariant(u'24x24'))
        comboModel.setData(comboModel.index(9, 0), QVariant(u'G4'))
        comboModel.setData(comboModel.index(9, 1), QVariant(u'48x48'))
        comboModel.setData(comboModel.index(10, 0), QVariant(u'G5'))
        comboModel.setData(comboModel.index(10, 1), QVariant(u'16x32'))
        comboModel.setData(comboModel.index(11, 0), QVariant(u'G6'))
        comboModel.setData(comboModel.index(11, 1), QVariant(u'24x48'))

        self.tbl_scale.setItemDelegateForColumn(2, FontDelegate(comboModel, self.tbl_scale))
        self.tbl_scale.setItemDelegateForColumn(4, FontDelegate(comboModel, self.tbl_scale))
        self.tbl_scale.setItemDelegateForColumn(6, FontDelegate(comboModel, self.tbl_scale))
        self.tbl_scale.setItemDelegateForColumn(8, FontDelegate(comboModel, self.tbl_scale))

        # model.appendRow([
        #     QStandardItem('192.168.1.1'),
        #     QStandardItem('1'),
        #     QStandardItem('11'),
        #     QStandardItem('aa'),
        #     QStandardItem('other')])
        # model.appendRow([
        #     QStandardItem('192.168.1.2'),
        #     QStandardItem('2'),
        #     QStandardItem('22'),
        #     QStandardItem('bb'),
        #     QStandardItem('other')])

        # model.setData(model.index(0, 0, QModelIndex()), QVariant(133))
        # model.setData(model.index(1, 0, QModelIndex()), QVariant(134))
        # model.setData(1, QVariant(33))

        # print model.data(model.index(0, 0, QModelIndex())).toPyObject()
        # print model.data(model.index(1, 0, QModelIndex())).toPyObject()

        # d = model.data(QModelIndex(0)).toUInt()
        # print d

        # print self.tbl_scale.selectionModel().item(0)
        # model.removeRow(0)

        self.tbl_scale.setModel(model)
        self.tbl_scale.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        # table.setItemDelegateForColumn(0, DBComboBoxDelegate(comboModel, table))
        self.tbl_scale.horizontalHeader().setStretchLastSection(True)
        # header = self.tbl_scale.horizontalHeader()
        # header.setResizeMode(0, QtGui.QHeaderView.Fixed)
        # header.setResizeMode(1, QtGui.QHeaderView.Stretch)
        # header.setResizeMode(2, QtGui.QHeaderView.Stretch)
        # header.setResizeMode(3, QtGui.QHeaderView.Stretch)
        # header.setResizeMode(4, QtGui.QHeaderView.Stretch)
        # header.setResizeMode(5, QtGui.QHeaderView.Custom)
        self.tbl_scale.setColumnWidth(0, 150)
        self.tbl_scale.setColumnWidth(1, 100)
        self.tbl_scale.setColumnWidth(2, 120)
        self.tbl_scale.setColumnWidth(3, 80)
        self.tbl_scale.setColumnWidth(4, 120)
        self.tbl_scale.setColumnWidth(5, 200)
        self.tbl_scale.setColumnWidth(6, 120)
        self.tbl_scale.setColumnWidth(7, 100)
        self.tbl_scale.setColumnWidth(8, 120)
        # self.tbl_scale.setColumnHidden(5, True)

        self.tbl_scale.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tbl_scale.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.tbl_scale.setItemDelegateForColumn(0, ScaleIPDelegate(self))

        self.edt_scaleno.setEnabled(False)
        # self.comboBox.setEnabled(False)

        # common.log_init()

    def setFontComboBox(self, combo_box):
        combo_box.setItemText(0, _translate("Dialog", "S1", None))
        combo_box.setItemText(1, _translate("Dialog", "S2", None))
        combo_box.setItemText(2, _translate("Dialog", "S3", None))
        combo_box.setItemText(3, _translate("Dialog", "S4", None))
        combo_box.setItemText(4, _translate("Dialog", "S5", None))
        combo_box.setItemText(5, _translate("Dialog", "S6", None))
        combo_box.setItemText(6, _translate("Dialog", "G1", None))
        combo_box.setItemText(7, _translate("Dialog", "G2", None))
        combo_box.setItemText(8, _translate("Dialog", "G3", None))
        combo_box.setItemText(9, _translate("Dialog", "G4", None))
        combo_box.setItemText(10, _translate("Dialog", "G5", None))
        combo_box.setItemText(11, _translate("Dialog", "G6", None))

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "寺冈秤文本下发工具 - " + self.main_dialog.getParams()["scaleType"], None))
        self.label.setText(_translate("Dialog", "秤列表", None))
        self.btn_send.setText(_translate("Dialog", "发送", None))
        self.label_2.setText(_translate("Dialog", "默认选项", None))
        self.label_3.setText(_translate("Dialog", "文本1(秤号)", None))
        self.label_4.setText(_translate("Dialog", "文本2(店号)", None))
        self.label_8.setText(_translate("Dialog", "文本3(店名)", None))
        self.label_9.setText(_translate("Dialog", "文本4(其它)", None))

        #self.edt_storeno.setText(_translate("Dialog", "1234", None))
        self.edt_storename.setText(_translate("Dialog", "店1", None))

        self.setFontComboBox(self.comboBox)
        self.setFontComboBox(self.comboBox_2)
        self.setFontComboBox(self.comboBox_3)
        self.setFontComboBox(self.comboBox_4)

        self.comboBox.setCurrentIndex(self.comboBox.findText("G1"))
        self.comboBox_2.setCurrentIndex(self.comboBox_2.findText("G1"))
        self.comboBox_3.setCurrentIndex(self.comboBox_3.findText("G1"))
        self.comboBox_4.setCurrentIndex(self.comboBox_4.findText("G1"))

if __name__ == "__main__":
    import sys
    # import icon_rc
    # icon_rc.qInitResources()
    app = QtGui.QApplication(sys.argv)
    Dialog = MyDialog()
    ui = Ui_TextToolDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

