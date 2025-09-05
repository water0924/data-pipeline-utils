from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidget, QTabWidget, QWidget, QVBoxLayout
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QThread,Signal,QTimer
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QPushButton
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QSizePolicy
import platform
import os
import requests


current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取当前 Ubuntu 系统的版本信息
ubuntu_version = platform.version()
print("Unsupported Ubuntu version:", ubuntu_version)

# 判断 Ubuntu 版本并动态导入对应模块
if "18.04" in ubuntu_version:
    # 如果是 Ubuntu 18.04，导入 python2_print_topic_data
    from print_topic_data.print_topic_data import topic_proto_map, PrintMessageData
elif "20.04" in ubuntu_version:
    # 如果是 Ubuntu 20.04，导入 python3_print_topic_data
    from print_topic_data.python3_print_topic_data import topic_proto_map, PrintMessageData
else:
    print("Unsupported Ubuntu version:", ubuntu_version)




import json
import time
import requests
import subprocess
from qcombocheckbox import ComboCheckBox
from file_selector import FileSelectorApp


class Stats:
    def __init__(self):
        self.ui = QUiLoader().load("blc_download.ui")
        self.env_file_path = ".env"
        self.ui.pushButton.clicked.connect(self.start_download)
        self.ui.pushButton_2.clicked.connect(self.click_open_file_button)
        self.ui.comboBox.currentIndexChanged.connect(self.update_comboBox_2)
        self.ui.pushButton_3.clicked.connect(self.start_print_data)
        self.update_comboBox_2(0)    
        tab_widget = self.ui.findChild(QTabWidget, "tabWidget")

        # 找到特定的 Tab
        tab2 = tab_widget.findChild(QWidget, "tab_2")

        self.combocheckBox = ComboCheckBox(sorted(list(topic_proto_map.keys())))
        self.combocheckBox.setParent(tab2)
        self.combocheckBox.setGeometry(QtCore.QRect(10, 210, 560, 30))
        self.combocheckBox.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        self.combocheckBox.setMinimumSize(QtCore.QSize(200, 30))

        self.fileSelectorApp = FileSelectorApp()
        self.fileSelectorApp.setParent(tab2)
        # # 将文件选择器的中心部件设置为 Tab 的内容
        # tab2.layout = QVBoxLayout(tab2)
        # tab2.layout.addWidget(self.fileSelectorApp)
        # tab2.layout.addWidget(self.combocheckBox)
        # tab2.setLayout(tab2.layout)

        # 创建一个定时器，用于定期刷新文本框
        self.timer = QTimer(self.ui)
        # self.timer.timeout.connect(self.refresh_text_edit)
        self.timer.timeout.connect(self.refresh_text_edit2)
        self.timer.start(1000)  # 每100毫秒刷新一次


    def update_comboBox_2(self,index):
        """根据第一个下拉框的选项更新第二个下拉框的选项"""
        self.ui.comboBox_2.clear()  # 清空第二个下拉框的选项
        self.ui.comboBox_2.addItem("缺陷")
        if index == 4:  
            self.ui.comboBox_2.addItem("吉利问题SWIM")

    def update_env_file(self):
        """
        更新.env文件中的变量值

        :param self.env_file_path: .env文件的路径
        """
        new_endpoint = self.ui.comboBox_3.currentText()
        new_output_dir = self.ui.lineEdit.text()
        new_only_download_log = self.ui.comboBox_4.currentText()
        if new_only_download_log == "否":
            new_only_download_log = "false"
        else:
            new_only_download_log = "true"

        work_item_lable_and_type_key_map ={
            "L2_parking":{"project_key":"6489578d34ebb6b41eb3f0f2","缺陷":"issue"},
            "L2_security":{"project_key":"64897f46c3555f243a4f17bb","缺陷":"issue"},
            "L2_driving":{"project_key":"6476e940445795f3885422e7","缺陷":"issue"},
            "c_01":{"project_key":"66e10434a2f32ff3b0cdb32b","缺陷":"681329d725ac1e8647ae80bd"},
            "gl_project":{"project_key":"675944fe83d50ba6e6577086","缺陷":"681329d725ac1e8647ae80bd","吉利问题SWIM":"67d0efd964eb651488678a30"},
            "tank":{"project_key":"675a471191bd0f8d353cd1ce","缺陷":"681329d725ac1e8647ae80bd"},
	        "DE09&C01-t":{"project_key":"675a485591bd0f8d353cd1d0","缺陷":"681329d725ac1e8647ae80bd"},
            "iffcom":{"project_key":"6819a4619743600eac42919f","缺陷":"681329d725ac1e8647ae80bd"}
        }
        work_name = self.ui.comboBox.currentText()
        work_item_label = self.ui.comboBox_2.currentText()
        print(work_item_label)
        new_project_key = work_item_lable_and_type_key_map[work_name]["project_key"]
        new_work_item_type_key = work_item_lable_and_type_key_map[work_name][work_item_label]
        updates = {
            'endpoint': new_endpoint,
            'output_dir': new_output_dir,
            'only_download_log': new_only_download_log,
            'project_key': new_project_key,
            'work_item_type_key':new_work_item_type_key,
        }
        print(updates)
        try:
            with open(self.env_file_path, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                for key, value in updates.items():
                    if line.startswith(key + '='):
                        line = f"{key}={value}  # {line.split('  # ')[1]}"
                updated_lines.append(line)

            with open(self.env_file_path, 'w') as file:
                file.writelines(updated_lines)

            print(f"成功更新.env文件：{self.env_file_path}")
        except FileNotFoundError:
            print(f"文件未找到：{self.env_file_path}")
        except Exception as e:
            print(f"发生错误：{e}")

    def start_download(self):
        self.update_env_file()
        issue_path = self.ui.lineEdit.text()
        issue_id = self.ui.lineEdit_2.text()
        self.fileSelectorApp.send_issue_path(issue_path+"/"+issue_id)
        """执行 Python 脚本并捕获输出"""
        # 清空文本框
        self.ui.textEdit.clear()

        # 创建并启动线程
        self.thread = ScriptExecutionThread(issue_id)  # 替换为你的脚本路径
        self.thread.output_signal.connect(self.update_text_edit)  # 绑定信号到槽
        self.thread.finished_signal.connect(self.update_tag_time)
        self.thread.start()

    def start_print_data(self):
        issue_id = self.ui.lineEdit_2.text()
        """执行 Python 脚本并捕获输出"""
        # 清空文本框
        self.ui.textEdit_2.clear()

        # # 创建并启动线程
        self.thread = WorkerThread(self.print_message_data)  # 替换为你的脚本路径
        self.thread.output_signal.connect(self.update_text_edit2)  # 绑定信号到槽
        self.thread.start()

    def update_text_edit(self, output):
        """更新文本框内容"""
        self.ui.textEdit.append(output)

    def update_text_edit2(self, output):
        """更新文本框内容"""
        self.ui.textEdit_2.append(output)

    def refresh_text_edit(self):
        """定期刷新文本框内容"""
        self.ui.textEdit.viewport().update()

    def refresh_text_edit2(self):
        """定期刷新文本框内容"""
        self.ui.textEdit_2.viewport().update()
    
    def update_tag_time(self):
        issue_path = self.ui.lineEdit.text()
        tag_id_path = issue_path + "/tag_id_path.json"
        if tag_id_path:
            with open(tag_id_path, encoding='utf-8') as f:
                extracted_ids = json.load(f)['extracted_ids']

        # 1. 把这里的 id 换成真实值
        url = f"https://drplatform-backend.deeproute.cn/scene/tag/instance/{extracted_ids}/"

        # 2. 如果接口需要登录态，取消下一行的注释并换成自己的 Cookie/Token
        # headers = {"Cookie": "sessionid=xxxxxxxxx"}
        headers = {}   # 目前为空，表示不带任何额外请求头

        # 3. 发送 GET 请求
        resp = requests.get(url, headers=headers, timeout=15)

        # 4. 打印返回结果
        try:
            # 优先按 JSON 解析
            data = resp.json() 
            body = data["body"]  
        except ValueError:
            # JSON 解析失败则直接打印文本
            print(resp.text)
            
        from datetime import datetime, timedelta, timezone

        ts_us = body["systemTime"]          # 微秒
        dt_utc = datetime.fromtimestamp(ts_us / 1e6, tz=timezone.utc)
        dt_cn  = dt_utc.astimezone(timezone(timedelta(hours=8))).isoformat()
        self.ui.lineEdit_3.setText(dt_cn)


    def print_message_data(self,output_signal):
        issue_path = self.fileSelectorApp.get_issue_path()
        chance_topic =self.combocheckBox.currentText()
        for topic_name in chance_topic:
            if "18.04" in ubuntu_version:
                output_signal.emit(f"解析{topic_name}中，勿动......")
                script_path = os.path.join(current_dir,"print_topic_data","print_topic_data.py")
                subprocess.run(["python2", script_path, issue_path,topic_name])
                output_signal.emit(f"大吉大利，打印完成......")
            else:
                output_signal.emit(f"解析{topic_name}中，勿动......")
                PrintMessageData(issue_path,topic_name)
                output_signal.emit(f"大吉大利，打印完成......")


    def click_open_file_button(self):
        """点击打开vscode文件按钮"""
        command = self.ui.lineEdit.text()+"/"+self.ui.lineEdit_2.text()
        subprocess.Popen(["code", command])


        

class ScriptExecutionThread(QThread):
    """用于执行脚本的线程"""
    output_signal = Signal(str)  # 定义信号，用于将输出发送到主线程
    finished_signal = Signal()  

    def __init__(self,issue_id):
        super().__init__()
        self.issue_id =issue_id

    def run(self):
        """执行脚本并捕获输出"""
        process = subprocess.Popen(
            ["blc_tools", "download_issue_attachments", self.issue_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        while True:
            output = process.stdout.readline()
            if output == "" and process.poll() is not None:
                break
            if output:
                self.output_signal.emit(output.strip())  # 发送输出信号

        process.wait()
        self.finished_signal.emit() 


class WorkerThread(QThread):
    # 定义一个信号，用于将输出内容发送到主线程
    output_signal = Signal(str)
    

    def __init__(self, function):
        super().__init__()
        self.function = function

    def run(self):
        # 调用传入的函数，并捕获打印的内容
        import io
        import sys
        old_stdout = sys.stdout
        sys.stdout = mystdout = io.StringIO()
        try:
            self.function(self.output_signal)
        finally:
            sys.stdout = old_stdout
        # 将捕获的输出内容通过信号发送到主线程
        self.output_signal.emit(mystdout.getvalue())



if __name__ == "__main__":
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec_()
