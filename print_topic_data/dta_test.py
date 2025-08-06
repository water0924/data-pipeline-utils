#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2024/8/22 下午1:49
# @Author  : shulongzhu
# @File    : dta_test.py
import subprocess
import os
import time

# 设置 ROS 环境变量
ros_setup_script = '/opt/ros/noetic/setup.bash'
# base_dir = "/media/jiangshuigen/JIERU03/0819dta数据采集/APA泊入泊出"
# dta_path = os.path.join(base_dir, "old_data")
# filter_path = os.path.join(base_dir,  "filter_data")
# record_path = os.path.join(base_dir, "new_data")


def play_rosbag(filter_path,name):
    work_path = os.path.join(filter_path, name)
    cmd = f"rosbag play {work_path}"
    return subprocess.Popen(cmd, shell=True, executable='/bin/bash')


def filter_rosbag(dta_path,filter_path,name):
    input_bag = os.path.join(dta_path, name)
    output_bag = os.path.join(filter_path, name)
    filter_expression = "topic!='/gwm/hmi_object' and topic!='/gwm/hmi_rasmap' and topic !='/gwm/havp_map' and topic !='/gwm/havp_vehicle'"
    cmd = f"rosbag filter {input_bag} {output_bag} \"{filter_expression}\""
    print(f"Executing command: {cmd}")

    # 执行命令
    process = subprocess.Popen(cmd, shell=True, executable='/bin/bash')
    process.wait()  # 等待命令执行完成


def record_rosbag(record_path,name):
    name = "new_" + name
    work_path = os.path.join(record_path, name)
    cmd = f"rosbag record -O {work_path}  -a"
    return subprocess.Popen(cmd, shell=True, executable='/bin/bash')


def list_files(directory):
    try:
        # 获取文件夹下所有文件名
        files = os.listdir(directory)
        # 过滤出文件，排除目录
        files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
        return files
    except Exception as e:
        print(f"Error: {e}")
        return []


def main():
    gen_path="/home/jiangshuigen/Downloads/dta_test_script/test"
    all_entries = os.listdir(gen_path)
    subfolders = [entry for entry in all_entries if os.path.isdir(os.path.join(gen_path, entry))]
    for base_dir in subfolders:
        # print(base_dir)
        dta_path = os.path.join(gen_path, base_dir, "old_data")
        filter_path = os.path.join(gen_path, base_dir,  "filter_data")
        record_path = os.path.join(gen_path, base_dir, "new_data")
        res =sorted(list_files(dta_path))
        #res = res[0:1]
        for name in res:
            print(name)
            filter_rosbag(dta_path,filter_path,name)
            time.sleep(2)
            print("开始录制数据")
            record_process = record_rosbag(record_path,name)
            print("开始播放数据")
            play_process = play_rosbag(filter_path,name)
            try:
                play_process.wait()  # 等待播放完成
            except KeyboardInterrupt:
                print("播放被中断")
            finally:
                record_process.terminate()  # 确保录制在播放完成后停止
                record_process.wait()
                print("录制完成")


if __name__ == "__main__":
    main()
    # gen_path="/media/jiangshuigen/JIERU03/0819dta数据采集"
    # all_entries = os.listdir(gen_path)
    # subfolders = [entry for entry in all_entries if os.path.isdir(os.path.join(gen_path, entry))]
    # for base_dir in subfolders:
    #     dta_path = os.path.join(gen_path, base_dir, "old_data")
    #     filter_path = os.path.join(gen_path, base_dir,  "filter_data")
    #     record_path = os.path.join(gen_path, base_dir, "new_data")
    #     print(dta_path,filter_path,record_path)
