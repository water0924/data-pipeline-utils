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
import argparse


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, "proto"))

from canbus import car_info_pb2,canbus_blc_state_pb2,dtu_canbus_interface_pb2,dtu_hmi_canbus_interface_pb2
from routing import local_routing_pb2
from drapi import command_pb2,notification_pb2,operation_status_pb2,vehicle_status_pb2,render_context_pb2
from common.vehicle_state import vehicle_state_pb2
from control import control_cmd_pb2
from planning import planning_business_interface_pb2
from lock_on_road import lock_on_road_pb2
from routing import routing_pb2
from perception import deeproute_perception_camera_pb2,deeproute_perception_rear_warning_pb2,deeproute_perception_ras_map_pb2,perception_dtu_interface_pb2
from drivers.gnss import ins_pb2
from app import deeproute_app_access_pb2
from avm import avm_pb2
from drdtu import dtu_command_pb2
from map import deeproute_map_ras_map_plus_pb2
from localization import localization_external_command_pb2,localization_external_events_pb2
from aeb import aeb_state_pb2
from common import module_event_pb2
from someip_adapter import avp_pb2
from safety import safety_analysis_pb2,state_exchange_pb2
from drapi.gwm.havp import havp_vehicle_pb2,havp_map_pb2
from smart import smart_business_pb2,smart_command_pb2
from smart.parking import smart_parking_frame_data_pb2,smart_lp_parking_map_pb2





topic_proto_map = {
    "/canbus/car_info": car_info_pb2.CarInfo(),
    "/local_routing/local_routing_inf": local_routing_pb2.LocalRouting(),
    "/blc/command": command_pb2.Command(),
    "/canbus/car_state": vehicle_state_pb2.VehicleState(),
    "/control/control_command": control_cmd_pb2.ControlCommand(),
    "/planner/event": planning_business_interface_pb2.PlanningEvent(),
    "/localization/lock_on_road": lock_on_road_pb2.LockOnRoadResult(),
    "/planner/response": planning_business_interface_pb2.PlanningResponse(),
    "/map/routing/response": routing_pb2.RoutingResponse(),
    "/perception/adas": deeproute_perception_camera_pb2.CameraStatus(),
    "/perception/rearwarning": deeproute_perception_rear_warning_pb2.RearWarningStatus(),
    "/perception/camera_quality": deeproute_perception_camera_pb2.CameraQuality(),
    "/sensors/gnss/pose": ins_pb2.SensorsIns(),
    "/app/info": deeproute_app_access_pb2.AppInfo(),
    "/avm/command_response": avm_pb2.AvmCommandRP(),
    "/dtu/command_response": dtu_command_pb2.DTUCMDRP(),
    "/perception/ras_map": deeproute_perception_ras_map_pb2.RASMap(),
    "/map/ras_map_plus": deeproute_map_ras_map_plus_pb2.RASMapPlus(),
    "/perception/dtu_response": perception_dtu_interface_pb2.PerceptionResponse(),
    "/localization/command_response": localization_external_command_pb2.LocalizationResponse(),
    "/localization/event": localization_external_events_pb2.LocalizationEvent(),
    "/aeb/aeb_state": aeb_state_pb2.StateWrapper(),
    "/dtu/command": dtu_command_pb2.DTUCMD(),
    "/planner/request": planning_business_interface_pb2.PlanningRequest(),
    "/map/routing/request": routing_pb2.RoutingRequest(),
    "/blc/command_response": command_pb2.CommandRP(),
    "/blc/event": notification_pb2.EventInfo(),
    "/blc/operation_status": operation_status_pb2.OperationStatus(),
    "/blc/local_routing_info": local_routing_pb2.LocalRouting(),
    "/avm/command": avm_pb2.AvmCommand(),
    "/perception/dtu_request": perception_dtu_interface_pb2.PerceptionRequest(),
    "/localization/command": localization_external_command_pb2.LocalizationCommand(),
    "/blc/device_status": vehicle_status_pb2.DeviceStatus(),
    "/blc/can_state_machine": canbus_blc_state_pb2.CanStateMachine(),
    "/common/module_events": module_event_pb2.ModuleEvents(),
    "/dtu/dtu_to_canbus_request": dtu_canbus_interface_pb2.DtuToCanbusRequest(),
    "/gwm/havp_path_info": avp_pb2.HAVPPathInfo(),
    "/gwm/havp_renderg_info": avp_pb2.HAVPRendergInfo(),
    "/gwm/havp_path_map": avp_pb2.HAVPPathMap(),
    "/gwm/havp_map_upd_st": avp_pb2.PrkgLotMapUpdSt(),
    "/gwm/havp_svp_swt_req": avp_pb2.HAVP_SVPSwtReq(),
    "/gwm/havp_prkg_typ_req": avp_pb2.PrkgTypReq(),
    "/gwm/havp_prkg_flr_req": avp_pb2.PrkgFlrReq(),
    "/gwm/havp_prkg_slot_req": avp_pb2.PrkgSlotReq(),
    "/gwm/havp_prkg_area_req": avp_pb2.PrkgAreaReq(),
    "/gwm/havp_lvng_poi_req": avp_pb2.LvngPOIReq(),
    "/gwm/havp_tar_prkg_id_req": avp_pb2.TarPrkgIDReq(),
    "/gwm/havp_near_slot_id_req": avp_pb2.NearSlotIDReq(),
    "/gwm/havp_function_req": avp_pb2.HAVPReq(),
    "/gwm/havp_auto_push_req": avp_pb2.AutoReq(),
    "/gwm/havp_svp_function_req": avp_pb2.SVPReq(),
    "/gwm/havp_avm_sts_req": avp_pb2.AVMDispReq(),
    "/gwm/havp_avm_sts_resp": avp_pb2.AVMDispResp(),
    "/gwm/havp_svp_scrn_info": avp_pb2.HAVP_SVPScrnInfoStruct(),
    "/safety/analysis": safety_analysis_pb2.SafetyAnalysis(),
    "/safety/mcu_status": state_exchange_pb2.SSMState(),
    "/dtu/dtu_hmi_to_canbus_request": dtu_hmi_canbus_interface_pb2.DtuHmiToCanbusRequest(),
    "/gwm/havp_vehicle": havp_vehicle_pb2.AVPVehicleData(),
    "/gwm/havp_map": havp_map_pb2.AVPMapData(),
    "/blc/smart_business_data": smart_business_pb2.SmartBusinessData(),
    "/smart/parking_frame": smart_parking_frame_data_pb2.ParkingFrameData(),
    "/smart/lp_command": smart_command_pb2.SmartCommandReq(),
    "/blc/render_context": render_context_pb2.RenderContext(),
    "/smart/lp_map": smart_lp_parking_map_pb2.MapInfoList(),
    "/gwm/someip_adapter/slot_id_report":avp_pb2.SlotIDReport()
}


def main():
  
  support_topic = "\n".join(topic_proto_map.keys())
  parser = argparse.ArgumentParser(description="Topic数据解析命令行参数,暂支持如下Topic:{}".format(support_topic))

  parser.add_argument('bag_path', type=str, help='需要解析的bag或存放bag路径')
  parser.add_argument('topic_name', type=str, help='需要解析Topic名称')
  
  args = parser.parse_args()
  
  PrintMessageData(args.bag_path,args.topic_name)
 
 
 
  
def PrintMessageData(bag_path,topic_name):
    if topic_name not in topic_proto_map:
          print('错误: topic {} 没有对应的消息类型映射！'.format(topic_name))
          return
    bag_path = os.path.abspath(bag_path)
    all_bag=[]
    if  bag_path.endswith(".bag"):
      all_bag.append(bag_path)
      # print_data_path = "/"+"/".join(bag_path.split("/",-1)[:-1])+"/"
    else:
      files = os.listdir(bag_path)
      files = [f for f in files if os.path.isfile(os.path.join(bag_path, f)) and f.endswith(".bag")]
      for bag_name in files:
        tmp_bag_path = os.path.join(bag_path, bag_name)
        all_bag.append(tmp_bag_path)


    for bag in all_bag:
      print_data_name=bag.split(".")[0]+"_"+topic_name.split("/",-1)[-1]+".txt"
      print ('\n======== {} ========'.format(topic_name))
      n=1
      bag=rosbag.Bag(bag)
      for topic, msg, t in bag.read_messages(topics=[topic_name]):
        data_to_debug = topic_proto_map[topic_name]
        data_to_debug.ParseFromString(strip_header(msg.data))
      
        with open (print_data_name,"ab") as f:
          time_data=GetTimeString(t.to_time())+"\n"
          f.write("================第{}条msg================\n".format(n))
          f.write(time_data)
          f.write(str(data_to_debug))
          n=n+1

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


def GetTimeString(tt):
  dt_object = datetime.datetime.fromtimestamp(tt)
  return dt_object.strftime("%Y-%m-%d %H:%M:%S.%f")
os.environ['TZ'] = "UTC"

bag_start_time = 0




    
if __name__ == '__main__':
    main()
    