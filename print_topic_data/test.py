import sys
import time
from PySide2.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PySide2.QtCore import QThread, Signal

class WorkerThread(QThread):
    # 定义一个信号，用于将输出内容发送到主线程
    output_signal = Signal(str)

    def __init__(self, function):
        super().__init__()
        self.function = function

    def run(self):
        # 重定向 sys.stdout 到一个自定义的输出流
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()

        try:
            self.function(self.output_signal)
        finally:
            sys.stdout = old_stdout

        # 发送剩余的输出内容
        self.output_signal.emit(mystdout.getvalue())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 设置主窗口
        self.setWindowTitle("线程示例")
        self.resize(600, 400)

        # 创建中心部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # 创建 QTextEdit 用于显示输出内容
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.layout.addWidget(self.text_edit)

        # 创建 QPushButton 用于启动线程
        self.push_button_start = QPushButton("启动线程")
        self.push_button_start.clicked.connect(self.start_thread)
        self.layout.addWidget(self.push_button_start)

    def start_thread(self):
        # 创建并启动线程
        self.worker_thread = WorkerThread(self.example_function)
        self.worker_thread.output_signal.connect(self.update_text_edit)
        self.worker_thread.start()

    def example_function(self, output_signal):
        # 示例函数，打印一些内容
        for i in range(5):
            print(f"这是第 {i + 1} 行输出")
            output_signal.emit(f"这是第 {i + 1} 行输出\n")
            time.sleep(1)

    def update_text_edit(self, output):
        # 将输出内容显示在 QTextEdit 中
        self.text_edit.append(output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_thread = main_window
    main_window.show()
    sys.exit(app.exec_())