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
from drapi import gl_p177_downstream_chassis_pb2,gwm_tank_downstream_chassis_pb2
from drapi.gl import gl_hpa_map_pb2



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
    "/blc/algorithm_command_response": dtu_command_pb2.DTUCMDRP(),
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
    "/gwm/someip_adapter/slot_id_report":avp_pb2.SlotIDReport(),
    "/gwm/someip_adapter/havp_map_management_set":havp_map_pb2.AVPMapManage(),
    "/mcu_blc/chassis_detail":gl_p177_downstream_chassis_pb2.UpstreamChassis(),
    "/mcu_blc/chassis_detail_tank":gwm_tank_downstream_chassis_pb2.UpstreamChassisTank(),
    "/blc/downstream_chassis_tank":gwm_tank_downstream_chassis_pb2.DownstreamChassisTank(),
    "/blc/downstream_chassis":gl_p177_downstream_chassis_pb2.DownstreamChassis(),
    "/gl/hpa_map":gl_hpa_map_pb2.HpaMap(),
    "/gl/hpa_map_vis":gl_hpa_map_pb2.HpaMap(),
}
