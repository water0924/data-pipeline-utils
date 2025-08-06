# -*- coding: utf-8 -*-
import sys
import argparse
import rosbag
import numpy as np
import struct
import os
from google.protobuf import json_format
from google.protobuf.json_format import MessageToDict
import datetime
def strip_header(string_data):
    if len(string_data) < 4:
        return string_data
    if string_data[0] != "$" or string_data[1] != "$" or string_data[2] != "$" or string_data[3] != "$":
        # without header
        return string_data
    else:
        # with header
        prefix_size = 4
        header_size_field_size = 4
        info_size = prefix_size + header_size_field_size
        header_size = struct.unpack("I", string_data[prefix_size : prefix_size + header_size_field_size])[0]
        return string_data[info_size + header_size:]


# sys.path.append(
#     '/opt/deeproute/planning_prediction/include/proto/offboard/')
sys.path.append('/home/jiangshuigen/Downloads/dta_test_script/proto')
# sys.path.append(os.path.realpath('.'))

# from planning import planning_business_interface_pb2
# from localization import localization_external_command_pb2
# from drapi import command_pb2
# from drapi import notification_pb2
# from canbus import car_info_pb2
# from drivers.gnss import ins_pb2
# from map import routing_pb2
# from common.vehicle_state import vehicle_state_pb2
from gwm.havp import havp_vehicle_pb2
from gwm.havp import havp_map_pb2
from google.protobuf import text_format
from common import module_event_pb2
from drapi import render_context_pb2
from smart.parking import smart_parking_frame_data_pb2,smart_lp_parking_map_pb2
# parser = argparse.ArgumentParser(description='read bag and plot.')
# parser.add_argument("bag_name")

# args = parser.parse_args()
def GetTimeString(tt):
  dt_object = datetime.datetime.fromtimestamp(tt)
  return dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
os.environ['TZ'] = "UTC"

bag_start_time = 0

def PrintRoutingResponse(bag): 
    routing_response_amap_debug = []
    print '\n======== /map/routing/response ========'
    for topic, msg, t in bag.read_messages(topics=["/map/routing/response"]):
      data_to_debug = routing_pb2.RoutingResponse()
      data_to_debug.ParseFromString(strip_header(msg.data))
      

        # for item in list:
        #     if planning_request.HasField(item):
      print GetTimeString(t.to_time()), '\n',data_to_debug
      with open("routing_response.txt", "w") as f:
          f.write(text_format.MessageToString(data_to_debug))
      
      for pt in data_to_debug.routes[0].shape_points:
          routing_response_amap_debug.append([pt.lon, pt.lat])
      
    print routing_response_amap_debug


def PrintCarState(bag):
    routing_response_amap_debug = []
    print '\n======== /canbus/car_state ========'
    for topic, msg, t in bag.read_messages(topics=["/canbus/car_state"]):
      data_to_debug = vehicle_state_pb2.VehicleState()
      data_to_debug.ParseFromString(strip_header(msg.data))
      

        # for item in list:
        #     if planning_request.HasField(item):
      print GetTimeString(t.to_time()), '\n',data_to_debug


def PrintSensorIns(bag):
    pos_data = []
    print '\n======== /sensors/gnss/pose ========'
    for topic, msg, t in bag.read_messages(topics=["/sensors/gnss/pose"]):
        data_to_debug = ins_pb2.SensorsIns()
        data_to_debug.ParseFromString(strip_header(msg.data))

        # for item in list:
        #     if planning_request.HasField(item):
        print GetTimeString(t.to_time()), '\n',data_to_debug
        # pos_data.append([data_to_debug.imu_frame_position_llh.lon, data_to_debug.imu_frame_position_llh.lat])
    # print pos_data
def PrintBLCEvent(bag):
    print '\n======== /blc/event ========'
    for topic, msg, t in bag.read_messages(topics=["/blc/event"]):
        data_to_debug = notification_pb2.EventInfo()
        data_to_debug.ParseFromString(strip_header(msg.data))

        # for item in list:
        #     if planning_request.HasField(item):
        print GetTimeString(t.to_time()), '\n',data_to_debug

def PrintCarInfo(bag):
    print '\n======== /canbus/car_info ========'
    apa_active = False
    for topic, msg, t in bag.read_messages(topics=["/canbus/car_info"]):
        if bag_start_time == 0:
            bag_start_time = t.to_sec()
        car_info = car_info_pb2.CarInfo()
        car_info.ParseFromString(strip_header(msg.data))

        # for item in list:
        #     if planning_request.HasField(item):
        if apa_active != car_info.apa_report.apa.active:
          print round(t.to_sec() - bag_start_time, 2), '\t'," CarInfo ", apa_active, "\t=>\t", car_info.apa_report.apa.active
        apa_active = car_info.apa_report.apa.active


def PrintHavpVehicle(bag,data_path):
    print '\n======== /gwm/havp_vehicle ========'
    n=1
    for topic, msg, t in bag.read_messages(topics=["/gwm/havp_vehicle"]):
      data_to_debug = havp_vehicle_pb2.AVPVehicleData()
      data_to_debug.ParseFromString(strip_header(msg.data))
      # analysis_data = MessageToDict(data_to_debug, preserving_proto_field_name=True)
      with open (data_path,"ab") as f:
        time_data=GetTimeString(t.to_time())+"\n"
        f.write("================第{}条msg================\n".format(n))
        f.write(time_data)
        f.write(str(data_to_debug))
        n=n+1
        # for item in list:s
        #     if planning_request.HasField(item):
      # print GetTimeString(t.to_time()), '\n',data_to_debug
      
def PrintHavpMap(bag,data_path):
    print '\n======== /gwm/havp_map ========'
    n=1
    for topic, msg, t in bag.read_messages(topics=["/gwm/havp_map"]):
      data_to_debug = havp_map_pb2.AVPMapData()
      data_to_debug.ParseFromString(strip_header(msg.data))
      # analysis_data = MessageToDict(data_to_debug, preserving_proto_field_name=True)
      with open (data_path,"ab") as f:
        time_data=GetTimeString(t.to_time())+"\n"
        f.write("================第{}条msg================\n".format(n))
        f.write(time_data)
        f.write(str(data_to_debug))
        n=n+1

def PrintModuleEvents(bag,data_path):
    print '\n======== /common/module_events ========'
    n=1
    for topic, msg, t in bag.read_messages(topics=["/common/module_events"]):
      data_to_debug = module_event_pb2.ModuleEvents()
      data_to_debug.ParseFromString(strip_header(msg.data))
      # analysis_data = MessageToDict(data_to_debug, preserving_proto_field_name=True)
      with open (data_path,"ab") as f:
        time_data=GetTimeString(t.to_time())+"\n"
        f.write("================第{}条msg================\n".format(n))
        f.write(time_data)
        f.write(str(data_to_debug))
        n=n+1
        
def PrintRenderContex(bag,data_path):
    print '\n======== /blc/render_context ========'
    n=1
    for topic, msg, t in bag.read_messages(topics=["/blc/render_context"]):
      data_to_debug = render_context_pb2.RenderContext()
      data_to_debug.ParseFromString(strip_header(msg.data))
      # analysis_data = MessageToDict(data_to_debug, preserving_proto_field_name=True)
      with open (data_path,"ab") as f:
        time_data=GetTimeString(t.to_time())+"\n"
        f.write("================第{}条msg================\n".format(n))
        f.write(time_data)
        f.write(str(data_to_debug))
        n=n+1

def PrintParkingFrameData(bag,data_path):
    print '\n======== /smart/parking_frame ========'
    n=1
    for topic, msg, t in bag.read_messages(topics=["/smart/parking_frame"]):
      data_to_debug = smart_parking_frame_data_pb2.ParkingFrameData()
      data_to_debug.ParseFromString(strip_header(msg.data))
      # analysis_data = MessageToDict(data_to_debug, preserving_proto_field_name=True)
      with open (data_path,"ab") as f:
        time_data=GetTimeString(t.to_time())+"\n"
        f.write("================第{}条msg================\n".format(n))
        f.write(time_data)
        f.write(str(data_to_debug))
        n=n+1

def PrintLPMapData(bag,data_path):
    print '\n======== /smart/lp_map ========'
    n=1
    for topic, msg, t in bag.read_messages(topics=["/smart/lp_map"]):
      data_to_debug = smart_lp_parking_map_pb2.MapInfoList()
      data_to_debug.ParseFromString(strip_header(msg.data))
      # analysis_data = MessageToDict(data_to_debug, preserving_proto_field_name=True)
      with open (data_path,"ab") as f:
        time_data=GetTimeString(t.to_time())+"\n"
        f.write("================第{}条msg================\n".format(n))
        f.write(time_data)
        f.write(str(data_to_debug))
        n=n+1
    
if __name__ == '__main__':
    gen_path="/home/jiangshuigen/Downloads/下坡车位不显示"
    all_entries = os.listdir(gen_path)
    subfolders = [entry for entry in all_entries if os.path.isdir(os.path.join(gen_path, entry))]
    for base_dir in subfolders:
      dta_path = os.path.join(gen_path, base_dir, "old_data")
      record_path = os.path.join(gen_path, base_dir, "new_data")
      print_path = os.path.join(gen_path, base_dir, "print_data")
      for bag_path in [dta_path,record_path]:
        all_entries = os.listdir(bag_path)
        subfolders = [entry for entry in all_entries if os.path.isfile(os.path.join(bag_path, entry))]
        for bag_name in subfolders:
          data_path=print_path+"/"+bag_name.split(".")[0]+".txt"
          map_data_path =print_path+"/"+bag_name.split(".")[0]+"_map"+".txt"
          print_bag_data_path = os.path.join(bag_path, bag_name)
          print(print_bag_data_path)
          bag=rosbag.Bag(print_bag_data_path)
          # PrintParkingFrameData(bag,data_path)
          # PrintRenderContex(bag,data_path)
          # PrintModuleEvents(bag,data_path)
          # PrintLPMapData(bag,map_data_path)
    # bag = rosbag.Bag(args.bag_name)
          PrintHavpVehicle(bag,data_path)
    