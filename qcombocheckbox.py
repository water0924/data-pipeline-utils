import os
import shutil
import subprocess
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidget,QLineEdit,QComboBox, QListWidget, QCheckBox, QListWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets,QtCore
import datetime
import sys


class ComboCheckBox(QComboBox):
    """
    下拉复选框调用代码
        1.传入一个items列表,定义下拉框选项
        2.改变组件的位置
        3.定义下拉框父级
    """
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setPlaceholderText("请选择你需要打印数据的topic")
        self.qLineEdit.setReadOnly(False)
        self.qListWidget = QListWidget()
        self.qListWidget.setFixedHeight(400)
        for i in range(len(self.items)):
            self.qCheckBox.append(QCheckBox())
            self.qCheckBox[i].setText(self.items[i])
            item = QListWidgetItem(self.qListWidget)
            self.qListWidget.setItemWidget(item, self.qCheckBox[i])
            if i == 0:
                self.qCheckBox[i].stateChanged.connect(self.All)
            else:
                self.qCheckBox[i].stateChanged.connect(self.showMessage)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def Selectlist(self):
        Outputlist = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                Outputlist.append(self.qCheckBox[i].text())
        self.Selectedrow_num = len(Outputlist)
        return Outputlist

    def showMessage(self):
        Outputlist = self.Selectlist()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        show = ';'.join(Outputlist)
        self.qLineEdit.setText(show)

        if self.Selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.Selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif zhuangtai == 1:
            if self.Selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif zhuangtai == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)

    def currentText(self):
        text = QComboBox.currentText(self).split(';')
        if text.__len__() == 1:
            if not text[0]:
                return []
        return text
    
if __name__ == '__main__':
    items = ['Python', 'R', 'Java', 'C++', 'CSS']
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    comboBox1 = ComboCheckBox(items)
    comboBox1.setParent(Form)
    comboBox1.setGeometry(QtCore.QRect(10, 10, 100, 20))
    comboBox1.setMinimumSize(QtCore.QSize(100, 20))
    Form.show()
    sys.exit(app.exec_())