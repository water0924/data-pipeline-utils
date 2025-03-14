import os
import sys
import time
import re

import pytest
sys.path.append(os.path.realpath('.'))
# 项目当前文件目录路径
# _project_dir = os.path.dirname(os.path.abspath(__file__))
# 项目根目录目录路径
_project_dir = os.path.abspath(os.path.dirname(__file__))
print(_project_dir)
import_list = ['from app',
               'from avm',
               'from common',
               'from drapi',
               'from drrun',
               'from planning',
               'from ros',
               'from rd_access',
               'from internel',
               'from semantic_map',
               'from devices',
               'from aeb',
               'from calibration',
               'from canbus',
               'from church',
               'from control',
               'from database',
               'from drdtu',
               'from drivers',
               'from internel',
               'from localization',
               'from lock_on_road',
               'from map',
               'from perception',
               'from prediction',
               'from remote_takeover',
               'from routing',
               'from semantic_map',
               'from visualizer',
               'from idl',
               'from dsm',
               'from graph_match',
               'from dem',
               'from dtc',
               'from ess',
               'from perf_collector',
               'from recorder',
               'from safety',
               'from starter',
               'from trip',
               'from offboard',
               'from odd',
               'from gwm',
               'from smart'
               'from odd',
               'from esa',
               'from smart',
               'from someip_adapter'
               ]

class DealProto():

    @classmethod
    def get_proto(self):
        """
        获取指定文件夹下所有proto文件路径

        Returns:
            _type_: _description_
        """
        test_path = _project_dir + "/proto/"
        # print(test_path)
        file_list1 = []
        for root, _, files in os.walk(test_path):
            # print(root)
            for file in files:
                # print(file)
                if file.endswith(".proto"):
                    # dearl_proto(file)
                    woqu= root.replace(
                        "/Users/easonhe/blc-interface-test/proto/", '')+"/"+file
                    # print(test_path+woqu)
                    file_list1.append(woqu)
        class  Clazz:
            test_path = _project_dir + "/proto/"
            file_list = file_list1
        return Clazz
    
    @classmethod
    def deal_proto_digital(self,folder_path):
        """
        处理部分proto文件引用中文件夹为数字情况,删除引用为数字开头模块数字
        Args:
            folder_path (_type_): 传入需要处理文件夹
        """
        old_string = '3rd_access'
        new_string = 'rd_access'

        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as file:
                    file_content = file.read()
                if old_string in file_content:
                    file_content = file_content.replace(old_string, new_string)
                    with open(file_path, 'w') as file:
                        file.write(file_content)

    @classmethod
    def deal_digital_proto_files(self):
        """
        处理proto文件夹以数字开头的文件夹,去掉数字
        """
        # 获取文件夹路径
        parent_path = _project_dir + "/proto/"
        match_string = "3rd_access"
        # print(parent_path)
        dirs = os.listdir(parent_path)
        pattern = re.compile(r'^\d+')
        for dir in dirs:
                # 拼接文件夹的完整路径
            dir_path = os.path.join(parent_path, dir)
            # print(dir_path)
            # 检查路径是否为文件夹，且是否以数字开头            
            if os.path.isdir(dir_path) and pattern.match(dir):
                # 构造新的文件夹名称
                # print(dir_path)
                self.deal_proto_digital(dir_path)
                new_name = re.sub(pattern, '', dir)
                # 重命名文件夹
                os.rename(dir_path, os.path.join(parent_path, new_name))


    @classmethod
    def conversion_proto_file(self):
        """
        转换所有proto文件为Python识别文件
        """
        prefix = _project_dir + "/proto/"
        proto_list = self.get_proto().file_list
        test_path = self.get_proto().test_path
        shell = "python3.8 -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. "
        if test_path.find(f"{prefix}") != -1:
            shell1 = "cd "+ test_path+";"
        else:
            print("脚本执行路径错误，请检查")
        # print(shell1)
        for i in range(len(proto_list)):
            index = proto_list[i].find(prefix)
            if index != -1:
                proto_list[i] = proto_list[i][index+len(prefix):]
        # print(proto_list)
        for i in proto_list:
            test = shell + i
            # print(shell1+test)
            os.popen(shell1+test).readlines()

    @classmethod
    def deal_pyfile(self, file1):
        """
        去掉所有proto文件中,引用为数字开头的文件夹，并删除数字
        Args:
            file (_type_): _description_
        """
        # print(file)
        for str_name in import_list:
            # print(str_name)
            file = open(file1, "r+")
            # print(file1)
            content = file.read()
            im = str_name.split(' ')[0]
            im_name = str_name.split(' ')[1]
            new_content = content.replace(str_name, im+' proto.'+im_name)
            file.seek(0)
            file.write(new_content)
            file.truncate()
            file.close()

    @classmethod
    def process_proto_to_pyfile(self):
        """
        处理proto文件转为Python可识别文件后,研发框架与测试框架不兼容情况
        """
        test_path = self.get_proto().test_path
        for dirpath, dirnames, filenames in os.walk(test_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # print(file_path)
                if file_path.endswith(".py"):
                    self.deal_pyfile(file_path)



if __name__ == '__main__':
    dp = DealProto()
    dp.deal_digital_proto_files()
    dp.conversion_proto_file()
    dp.process_proto_to_pyfile()