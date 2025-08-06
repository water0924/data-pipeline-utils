import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,QLabel, QFileDialog, QWidget, QTreeView, QFileSystemModel, QAbstractItemView, QDialog, QVBoxLayout, QLabel, QPushButton
from PySide2.QtCore import Qt
from PySide2 import QtCore


class FileSelectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置主窗口
        self.setWindowTitle("文件或文件夹选择器")
        self.resize(600, 200)

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 创建 QLabel 作为拖动区域
        self.label_drag_area = QLabel("将文件或文件夹拖动到这里")
        self.label_drag_area.setAlignment(Qt.AlignCenter)
        self.label_drag_area.setStyleSheet("QLabel { border: 2px dashed #ccc; padding: 20px; font-size: 14px; color: #666; }")
        self.layout.addWidget(self.label_drag_area)

        # 创建 QLineEdit 用于显示文件或文件夹路径
        self.line_edit_path = QLineEdit()
        self.line_edit_path.setPlaceholderText("拖动文件或文件夹到这里或点击选择")
        # self.line_edit_path.setReadOnly(True)
        self.line_edit_path.setStyleSheet("QLineEdit { border: 1px solid #ccc; padding: 5px; font-size: 14px; }")
        self.layout.addWidget(self.line_edit_path)

        # 创建 QPushButton 用于点击选择文件或文件夹
        self.push_button_select = QPushButton("选择文件或文件夹")
        self.push_button_select.setStyleSheet("QPushButton { background-color: #0078d7; color: white; padding: 5px 10px; border-radius: 5px; } QPushButton:hover { background-color: #005ba1; }")
        self.push_button_select.clicked.connect(self.select_path)
        self.layout.addWidget(self.push_button_select)

        # 设置拖动事件
        self.label_drag_area.setAcceptDrops(True)
        self.label_drag_area.dragEnterEvent = self.drag_enter_event
        self.label_drag_area.dropEvent = self.drop_event

    def select_path(self):
        """点击按钮选择文件或文件夹"""
        # 弹出自定义对话框
        dialog = CustomFileDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            path = dialog.selected_path()
            self.line_edit_path.setText(path)

    def send_issue_path(self,path):
        self.line_edit_path.setText(path)
        
    def get_issue_path(self):
        issue_path = self.line_edit_path.text()
        return issue_path


    def drag_enter_event(self, event):
        """处理拖动进入事件"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """处理文件或文件夹拖动释放事件"""
        if event.mimeData().hasUrls():
            path = event.mimeData().urls()[0].toLocalFile()
            self.line_edit_path.setText(path)
            event.accept()
        else:
            event.ignore()


class CustomFileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择文件或文件夹")
        self.resize(800, 500)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.model = QFileSystemModel()
        self.model.setRootPath("/")  # 设置模型的根路径为根目录

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index("/"))  # 设置树形视图的根路径为根目录
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDragEnabled(True)
        self.tree_view.setDropIndicatorShown(True)
        self.tree_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.layout.addWidget(self.tree_view)

        # 初始时定位到主目录
        home_index = self.model.index(os.path.expanduser("~"))
        if home_index.isValid():
            self.tree_view.expand(home_index)  # 展开主目录
            self.tree_view.setCurrentIndex(home_index)  # 设置当前索引为主目录

        self.tree_view.header().resizeSection(0, 300)
        self.button_box = QHBoxLayout()  # 使用水平布局
        self.up_button = QPushButton("返回上一级")
        self.up_button.clicked.connect(self.go_up)  # 连接到返回上一级的方法
        self.select_button = QPushButton("选择")
        self.select_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        self.button_box.addWidget(self.up_button)
        self.button_box.addWidget(self.select_button)
        self.button_box.addWidget(self.cancel_button)
        self.layout.addLayout(self.button_box)

    def selected_path(self):
        index = self.tree_view.selectionModel().currentIndex()
        if index.isValid():
            return self.model.filePath(index)
        return ""

    def go_up(self):
        """返回上一级目录"""
        current_index = self.tree_view.currentIndex()
        if current_index.isValid():
            parent_index = current_index.parent()
            if parent_index.isValid():
                self.tree_view.setCurrentIndex(parent_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileSelectorApp()
    window.show()
    sys.exit(app.exec_())