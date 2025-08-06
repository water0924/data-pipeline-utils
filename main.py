import os,time
import shutil
import subprocess
from PySide2.QtWidgets import QApplication, QMessageBox, QTableWidget,QLineEdit,QComboBox, QListWidget, QCheckBox, QListWidgetItem,QMenu,QAction
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets,QtCore
from PySide2.QtCore import QTimer,QMetaObject,Signal,QThread,QRunnable,QThreadPool,Qt,QObject,QCoreApplication,QProcess,QSize, QEvent
from PySide2.QtGui import QMovie,QPixmap
import datetime
import sys
from qcombocheckbox import ComboCheckBox
import threading
import shlex



class Stats:
    def __init__(self):
        self.ui = QUiLoader().load(f"./main.ui")
        self.ui.pushButton_start.clicked.connect(self.start_simulation)
        self.ui.pushButton_stop.clicked.connect(self.stop_simulation)
        self.ui.pushButton_prophet.clicked.connect(self.start_prophet)
        self.ui.pushButton_log.clicked.connect(self.export_log)
        self.ui.pushButton_record.clicked.connect(self.start_record)
        self.ui.pushButton_package.clicked.connect(self.start_function)
        self.ui.pushButton_onboard.clicked.connect(self.click_onboard_button)
        self.ui.pushButton_phet.clicked.connect(self.click_prophet_button)
        self.ui.pushButton_vehicle.clicked.connect(self.click_vehicle_button)
        self.ui.docker_set_button.clicked.connect(self.click_docker_set_button)
        self.ui.pushButton_help.clicked.connect(self.show_help_dialog)
        self.ui.docker_help_button.clicked.connect(self.show_docker_help_dialog)
        self.update_progress = self.update_progress
        self.ui.label_8.setHidden(True) 
        self.movie = QMovie('./CSS/cheche.gif')
        self.ui.label_11.setMovie(self.movie)
        self.movie.setSpeed(50)
        self.movie.start()
        self.log_module()
        self.load_history_name()
        self.timer = QTimer()
        self.timer.timeout.connect(self.docker_status)
        self.timer.start(3000)

        items=self.get_topic()
        self.combocheckBox = ComboCheckBox(items)
        self.combocheckBox.setParent(self.ui)
        self.combocheckBox.setGeometry(QtCore.QRect(180, 560, 450, 25))
        self.combocheckBox.setMinimumSize(QtCore.QSize(200, 30))
        self.thread1=None
        self.thread2=None
        self.image_new=None
        # self.progresstimer=QTimer()
    def delete_all_docker(self):
        os.system("sudo docker rm -f prophet vehicle-model os-bridge onboard sensor-sim emulator carla")
    def delete_image(self):
        ads_name=self.get_ads_name().replace("=",":")
        os.system(f"sudo docker rmi {ads_name}")
    def start_function(self):
        if self.thread1 and self.thread1.isRunning():
            return
        if self.thread2 and self.thread2.isRunning():
            return
        self.thread1 = Function1Runner(self.ui)
        self.thread2 = Function2Runner(self.ui)
        self.thread1.progress_update.connect(self.update_progress)
        self.thread2.progress_update.connect(self.os_process)
        self.thread2.image_update.connect(self.update_image)
        self.thread1.finished.connect(self.enable_button)
        self.thread2.finished.connect(self.enble_sure)
        # self.thread.finished.connect(self.thread.deleteLater)

        self.ui.progressBar_pack.setValue(0)

        # button = self.findChild(QPushButton, "run-button")
        # button.setEnabled(False)

        self.thread1.start()
        self.thread2.start()

    def update_progress(self, value):
        self.ui.progressBar_pack.setValue(value)
    def os_process(self,value):
        self.ui.progressBar_pack.setValue(value)        
    def update_image(self,value):
         self.ui.lineEdit_new.setText(value)
    def enable_button(self):
        # print("完成了1")
        self.thread1.finished.connect(self.thread1.quit)
    def enble_sure(self):
        # print("完成了2")
        self.thread2.finished.connect(self.thread2.quit)   

    def send_mode(self):
        """
        1.获取并传入仿真的模式
        2.根据传入的模式替换docker-compose文件
        """
        mode=self.get_mode()
        mode_dict = {
            "深圳行车":"driving_shenzhen",
            "重庆行车":"driving_chongqing",
            "VPA学习":"vpa_study",
            "VPA巡航":"vpa_routing"
        }
        mode_dir = mode_dict[mode]
        # whether_debug = self.open_debug()
        # 进入终端和切换目录
        # os.chdir('/home/jiangshuigen/Documents/simulation_test')

        # 检查文件夹下是否存在docker-compose.yml文件
        if os.path.exists('docker-compose.yml'):
            # 删除docker-compose.yml文件
            os.remove('docker-compose.yml')
            print("已删除当前目录下的docker-compose.yml文件")

        # 复制docker-compose.yml文件到/simulation_test/文件夹下
        try:
                shutil.copy(f'./{mode_dir}/docker-compose.yml', './docker-compose.yml')
                print("文件复制成功")
        except Exception as e:
            QMessageBox.critical(self.ui, "错误", "docker-compose文件不存在")
            print(str(e)) 
            print("docker-compose文件不存在")
            raise
        except:
            print("复制文件时发生错误")
            return 

    def send_ads(self):
        """
        1.获取ads包名称
        2.将ads包替换环境变量文件
        3.修改Image
        4.修改日志等级
        """
        ads_name = self.get_ads_name().replace("=",":")
        log_level = self.open_debug()
        try:
            assert ads_name != ""
        except Exception as e:
            print(str(e))
            QMessageBox.critical(self.ui, "错误", "请输入正确的Ads包")
            raise
        brand = self.radioButtonSelected()
        if brand=="M5":
            file_path = './.env_m5'  # 文本文件路径
        elif brand=="GWM":
            file_path='./.env_gwm'
        result = os.system(f"sudo docker images --format '{{{{.Repository}}}}:{{{{.Tag}}}}' | grep {ads_name}")
        if result!=0:
            ads_name = ads_name.replace(":","=")
            new_pack = f'DRIVER_PACKAGE_VERSION={ads_name}\n'  # 新的首行内容
            new_image="DRIVER_IMAGE=reg.deeproute.ai/deeproute-all/cicd/driver-ubuntu1804-x86:7607270\n"
        else:
            new_pack = "DRIVER_PACKAGE_VERSION=\n"  # 新的首行内容
            new_image=f"DRIVER_IMAGE={ads_name}\n"
        # 打开文件并读取所有内容
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 删除前两行
        lines = lines[2:]

        # 在列表的开头插入新的行
        lines.insert(0, new_pack)
        lines.insert(1,new_image)
        if log_level=="非debug日志":
            print("非debug日志")
            lines[4]="#GLOG_v=1\n"
        else:
            print("debug日志")
            lines[4]="GLOG_v=1\n"
        # 将修改后的内容写回文件
        with open(file_path, 'w') as file:
            file.writelines(lines)

    # 启动prophet
    def start_prophet(self):
        os.system('gnome-terminal -- bash -c "prophet; exec bash"')
    
    # 导入日志模块
    def log_module(self):
        module = ["blc","control","lock_on_road","map_engine","perception","planning","sd_routing","safety","dem","dsm","全部"]
        for i in module:
            self.ui.comboBox_export.addItem(i)
        
    # 导出日志
    def export_log(self):
        module = self.ui.comboBox_export.currentText()
        log_path=self.ui.lineEdit_path.text()
        #os.system("sudo docker cp onboard:/ext_data/debug/logs/newest_dir ./")
        # with open("newest_dir","r") as file:
        #     lines = file.read()
        # current_date = lines.split("/")[-1]
        lines=os.popen("sudo docker exec onboard ls -tr /media/onboard/data/trips/").read().strip().split("\n")[-1]
        print(lines)
        current_date=lines.split("_",1)[-1]
        print(current_date)
        if log_path=="":
            if module=="全部":
                os.system("sudo docker cp onboard:/media/onboard/data/trips/{}/logs/ ~/log/{}/".format(lines,current_date))
            else: 
                os.system("sudo docker cp onboard:/media/onboard/data/trips/{}/logs/{}/ ~/log/{}/".format(lines,module,current_date))
        else:
            os.system("sudo docker cp onboard:{} ~/log/{}/".format(log_path,current_date))
        home_dir = os.path.expanduser("~")
        folder_path = f"{home_dir}/log/{current_date}"  # 替换为实际的文件夹路径
        print(folder_path)
        os.system(f"sudo nautilus --select {folder_path} &")


    
          

    # 获取仿真启动模式
    def get_mode(self):
        mode = self.ui.comboBox.currentText()
        return mode
    
    # 加载历史记录
    def load_history_name(self):
        file_name = './history.txt'
        with open(file_name, 'r') as file:
            lines = file.readlines()
        for i in lines:
            self.ui.comboBox_name.addItem(i)
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("请输入您的Ads包名称")
        line_edit.clear()  # 清空文本框的内容
        self.ui.comboBox_name.setLineEdit(line_edit)

        # 设置当前索引为-1
        self.ui.comboBox_name.setCurrentIndex(-1)

    # 获取Ads包名称
    def get_ads_name(self):
        ads_name = str(self.ui.comboBox_name.currentText()).strip()
        return ads_name

    def deal_history(self):
        file_name = './history.txt'
        ads_name = str(self.get_ads_name()).strip()
        new_ads = ads_name+'\n'
        if ads_name  != "":
            with open(file_name, 'r') as file:
                lines = file.readlines()
                # print(lines)
            if new_ads not in lines:
                self.ui.comboBox_name.insertItem(0, new_ads)
            if len(lines)<10 and new_ads not in lines:
                # print(new_ads)
                lines.insert(0, new_ads)
            if len(lines) >=10 and new_ads not in lines:
                lines.pop()
                lines.insert(0, new_ads)
            # 将修改后的内容写回文件
            with open(file_name, 'w') as file:
                file.writelines(lines)

        
    
    #获取topic
    def get_topic(self):
        with open("all_topic.txt","r") as f:
            line=f.readlines()
        all_topic=[]
        for i in line:
            topic=i.strip()
            all_topic.append(topic)
        return all_topic

    def jindu(self,int):
        self.ui.progressBar_pack.setValue(int)  

    # 打包镜像
    def package_image(self):
        for i in range(5):
            print("ddd")
            i=i-1
            time.sleep(5)
            if i==0:
                break

        # self.ui.progressBar_pack.setValue(10)
        # time.sleep(10)
        # version=self.ui.lineEdit_base.text().replace(":","=")
        # tem_image=version.replace("=","-")
        # tag = self.ui.lineEdit_tag.text()
        # if tag=="":
        #     tag=1.0
        # os.system(f"sudo docker exec -it onboard sudo apt install -y {version}")
        # os.system(f"sudo docker commit -a 'test' -m 'test' onboard reg.deeproute.ai/deeproute-modules-all/driver/{tem_image}:{tag}")
        # self.ui.progressBar_pack.setRange(0, 100)
        # self.ui.progressBar_pack.setValue(100)
        # self.ui.lineEdit_new.setText(f"{tem_image}:{tag}")



    #点击开始录制
    def start_record(self):
        # 获取选择的topic
        chance_topic =self.combocheckBox.currentText()
        print(chance_topic)
        new_chace_topic =" ".join(chance_topic).strip()
        print(new_chace_topic)
        if chance_topic == []:   
             os.system('gnome-terminal -- bash -c "cd ~;rosbag record -a; exec bash"')
        else:
             os.system(f'gnome-terminal -- bash -c "cd ~;rosbag record {new_chace_topic}; exec bash"')

    # 获取是否开启debug日志
    def open_debug(self):
        text=self.ui.comboBox_debug.currentText()
        # print(text)
        return text

    def radioButtonSelected(self):
        # 判断哪个 brand 被选中
        if self.ui.radioButton_1.isChecked():
            brand="M5"
        elif self.ui.radioButton_2.isChecked():
            brand="GWM"
        return brand
    
    def docker_status(self):
        # print("css")
        running = os.popen("sudo docker ps | awk '{print $NF}'").read().strip().split("\n")
        button={
            # "emulator":"pushButton_emulator",
            # "sensor-sim":"pushButton_sensor",
            "vehicle-model":"pushButton_vehicle",
            "onboard":"pushButton_onboard",
            # "os-bridge":"pushButton_bridge",
            # "carla":"pushButton_carla",
            "prophet":"pushButton_phet"
        }
        # all=['emulator', 'sensor-sim', 'vehicle-model', 'onboard', 'os-bridge', 'carla','prophet']
        all=[ 'vehicle-model', 'onboard','prophet']
        common_ele= list(set(running) & set(all))
        different_ele= list(set(running) ^ set(all))
        for b_key in common_ele:
            if b_key in all:
                b_button = getattr(self.ui, button[b_key])
                b_button.setStyleSheet("background-color: rgb(138, 226, 52);")
            else:
                pass
        for b_key in different_ele:
            if b_key in all:
                b_button = getattr(self.ui, button[b_key])
                b_button.setStyleSheet("background-color: rgb(239, 41, 41);")
            else:
                pass
        # for i in common_ele:
        #     press_button=button[i]
        #     if press_button=="pushButton_emulator":
        #         self.ui.pushButton_emulator.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     elif press_button=="pushButton_sensor":
        #         self.ui.pushButton_sensor.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     elif press_button=="pushButton_vehicle":
        #         self.ui.pushButton_vehicle.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     elif press_button=="pushButton_onboard":
        #         self.ui.pushButton_onboard.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     elif press_button=="pushButton_bridge":
        #         self.ui.pushButton_bridge.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     elif press_button=="pushButton_carla":
        #         self.ui.pushButton_carla.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     elif press_button=="pushButton_phet":
        #         self.ui.pushButton_phet.setStyleSheet("background-color: rgb(138, 226, 52);")
        #     else:
        #         pass
            
        # for j in different_ele:
        #     if j in all:
        #         press_button=button[j]
        #     # print(press_button)
        #         if press_button=="pushButton_emulator":
        #             self.ui.pushButton_emulator.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         elif press_button=="pushButton_sensor":
        #             self.ui.pushButton_sensor.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         elif press_button=="pushButton_vehicle":
        #             self.ui.pushButton_vehicle.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         elif press_button=="pushButton_onboard":
        #             self.ui.pushButton_onboard.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         elif press_button=="pushButton_bridge":
        #             self.ui.pushButton_bridge.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         elif press_button=="pushButton_carla":
        #             self.ui.pushButton_carla.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         elif press_button=="pushButton_phet":
        #             self.ui.pushButton_phet.setStyleSheet("background-color: rgb(239, 41, 41);")
        #         else:
        #             pass



    def show_dialog(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("提示")
        msg_box.setText("是否打包镜像")
        msg_box.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msg_box.setButtonText(QMessageBox.Yes, "是")
        msg_box.setButtonText(QMessageBox.No, "否")
        msg_box.setDefaultButton(QMessageBox.No)
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            ads_name=self.get_ads_name().replace("=",":")
            subprocess.run(["sudo", "docker", "commit", "-a", "test", "-m", "test", "onboard", f"{ads_name}"])
        elif result == QMessageBox.No:
            pass
        else:
            raise

    def show_help_dialog(self):
        msg = QMessageBox()
        custom_icon = QPixmap("./CSS/me.jpg")
        ustom_icon_resized = custom_icon.scaled(QSize(80, 80))
        msg.setIconPixmap(ustom_icon_resized)
        # msg.setIcon(QMessageBox.Information)
        text = "1、测试APA泊车可使用【VPA学习或VPA巡航】\n2、打包镜像前,需保证版本已下载安装完\n3、【删除镜像】是基于版本输入框内的ads版本进行删除\n有问题联系，Author: Shuigen Jiang\nversion：V20240127"
        msg.setText(text)
        msg.setWindowTitle("Help")
        msg.exec_()

    def show_docker_help_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        # msg.setIcon(QMessageBox.Information)
        text = "1、绿色代表容器已启动\n2、红色代表容器未启动\n3、单击按钮可选择进入容器或查看日志"
        msg.setText(text)
        msg.setWindowTitle("Help")
        msg.exec_()




    def click_vehicle_button(self):
        menu = QMenu(self.ui)
        self.action1 = QAction("进入vehicle容器")
        menu.addAction(self.action1)
        self.action1.triggered.connect(lambda: self.enter_docker("vehicle-model"))
        self.action2 = QAction("查看vehicle日志")
        menu.addAction(self.action2)
        self.action2.triggered.connect(lambda: self.check_docker_log("vehicle-model"))
        self.ui.pushButton_vehicle.setMenu(menu)

    def click_onboard_button(self):
        menu = QMenu(self.ui)
        self.action5 = QAction("进入onboard容器")
        menu.addAction(self.action5)
        self.action5.triggered.connect(lambda: self.enter_docker("onboard"))
        self.action6 = QAction("查看onboard日志")
        menu.addAction(self.action6)
        self.action6.triggered.connect(lambda: self.check_docker_log("onboard"))
        self.ui.pushButton_onboard.setMenu(menu)

    def click_prophet_button(self):
        menu = QMenu(self.ui)
        self.action7 = QAction("进入prophet容器")
        menu.addAction(self.action7)
        self.action7.triggered.connect(lambda: self.enter_docker("prophet"))
        self.action8 = QAction("查看prophet日志")
        menu.addAction(self.action8)
        self.action8.triggered.connect(lambda: self.check_docker_log("prophet"))
        self.ui.pushButton_phet.setMenu(menu)

        
    def check_docker_log(self,docker_name):
        os.system(f'gnome-terminal -- bash -c "sudo docker logs {docker_name} -f ; exec bash"')
    def enter_docker(self,docker_name):
        os.system(f'gnome-terminal -- bash -c "sudo docker exec -ti {docker_name} bash; exec bash"')

    def click_docker_set_button(self):
        menu = QMenu(self.ui.docker_set_button)
        self.action3 = QAction("删除所有容器")
        menu.addAction(self.action3)
        self.action3.triggered.connect(self.delete_all_docker)
        self.action4 = QAction("删除镜像")
        menu.addAction(self.action4)
        self.action4.triggered.connect(self.delete_image)
        self.ui.docker_set_button.setMenu(menu)


            

    def check_onboard_log(self):
        os.system('gnome-terminal -- bash -c "sudo docker logs onboard -f ; exec bash"') 

    def start_simulation(self):
        text = self.ui.pushButton_start.text()
        if text == "启动仿真":
            self.deal_history()
            self.send_mode()
            self.send_ads()
            brand=self.radioButtonSelected()
            if brand=="M5":
                os.system('gnome-terminal -- bash -c "sudo docker-compose --env-file .env_m5 up --force-recreate; exec bash"')
            elif brand=="GWM":
                os.system('gnome-terminal -- bash -c "sudo docker-compose --env-file .env_gwm up --force-recreate; exec bash"')
            self.ui.pushButton_start.setEnabled(False)
    def stop_simulation(self):
        text = self.ui.pushButton_stop.text()
        ads_name=self.get_ads_name().replace("=",":")
        result = os.system(f"sudo docker images --format '{{{{.Repository}}}}:{{{{.Tag}}}}' | grep '{ads_name}'")
        if text == "关闭仿真":
            if result !=0:
                self.show_dialog()
            os.system("sudo kill -9 `ps -ef | grep docker-compose | awk '{print $2}'`")
            os.system("sudo docker stop sensor-sim vehicle-model os-bridge onboard carla emulator prophet")
            self.ui.pushButton_start.setEnabled(True)

class Function1Runner(QThread):
    progress_update = Signal(int)
    finished = Signal(bool)
    def __init__(self,ui):
        super(Function1Runner, self).__init__()
        self.ui=ui
    def run(self):
        self.ui.progressBar_pack.setValue(0)
        for a in range(0,100):
            value = self.ui.progressBar_pack.value()
            value += 5
            if value > 90:
                value = 90
                self.finished.emit(True)
                break
            print(value)
            self.progress_update.emit(int(value))
            time.sleep(1)



class Function2Runner(QThread):
    progress_update = Signal(int)
    finished = Signal(bool)
    image_update= Signal(str)

    def __init__(self,ui):
        super(Function2Runner, self).__init__()
        self.ui=ui

    def run(self):
        self.ui.label_8.setHidden(False) 
        self.ui.label_8.setText("打包中...")
        self.progress_update.emit(0)
        version=self.ui.lineEdit_base.text().replace(":","=")
        tem_image=version.replace("=","-").replace(" ","")
        tag = self.ui.lineEdit_tag.text()
        if tag=="":
            tag=1.0
        # os.system(f"sudo docker exec -it onboard sudo apt install -y {version}")
        os.system("sudo docker exec -ti onboard sudo apt update")
        subprocess.run(["sudo", "docker", "exec", "-it", "onboard", "sudo", "apt", "install", "-y","--allow-downgrades"]+ shlex.split(version))
        self.progress_update.emit(80)
        subprocess.run(["sudo", "docker", "commit", "-a", "test", "-m", "test", "onboard", f"{tem_image}:{tag}"])
        # os.system(f"sudo docker commit -a 'test' -m 'test' onboard reg.deeproute.ai/deeproute-modules-all/driver/{tem_image}:{tag}")
        self.progress_update.emit(100)
        self.ui.label_8.setText("打包已完成")
        image_new=str(tem_image)+":"+str(tag)
        self.image_update.emit(image_new)
        # self.ui.lineEdit_new.setText(f"{tem_image}:{tag}")
        self.finished.emit(True)








if __name__=='__main__':   
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    # stats.load_history_name()
    # stats.set_press_button_style()
    app.exec_()
