package(features=['-hidden_visibility_feature'])
load("@rules_cc//cc:defs.bzl", "cc_proto_library")
load("@rules_proto_grpc//python:defs.bzl", "python_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")

proto_library(
  name = "basic_common_proto",
  srcs = ["basic_common.proto"],
  visibility = ["//visibility:public"],
  strip_import_prefix = "/proto/",
)

cc_proto_library(
  name = "basic_common_proto_cc",
  visibility = ["//visibility:public"],
  deps = [":basic_common_proto"],
)

python_proto_library(
  name = "basic_common_proto_py",
  visibility = ["//visibility:public"],
  protos = [":basic_common_proto"],
)

proto_library(
  name = "lp_control_command_proto",
  srcs = ["lp_control_command.proto"],
  deps = [":basic_common_proto", ":lp_common_proto"],
  visibility = ["//visibility:public"],
  strip_import_prefix = "/proto/",
)

cc_proto_library(
  name = "lp_control_command_proto_cc",
  visibility = ["//visibility:public"],
  deps = [":lp_control_command_proto"],
)

python_proto_library(
  name = "lp_control_command_proto_py",
  visibility = ["//visibility:public"],
  protos = [":lp_control_command_proto"],
)


proto_library(
  name = "lp_common_proto",
  srcs = ["lp_common.proto"],
  deps = [
    "@com_google_protobuf//:any_proto",
    "@com_google_protobuf//:wrappers_proto",
  ],
  visibility = ["//visibility:public"],
  strip_import_prefix = "/proto/",
)

cc_proto_library(
  name = "lp_common_proto_cc",
  visibility = ["//visibility:public"],
  deps = [":lp_common_proto"],
)

python_proto_library(
    name = "lp_common_proto_py",
    visibility = ["//visibility:public"],
    protos = [
        ":lp_common_proto",
    ],
)

proto_library(
  name = "lp_hmi_display_proto",
  srcs = ["lp_hmi_display.proto"],
  deps = [":lp_common_proto", ":basic_common_proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)

cc_proto_library(
  name = "lp_hmi_display_proto_cc",
  deps = [":lp_hmi_display_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_hmi_display_proto_py",
  protos = [":lp_hmi_display_proto"],
  visibility = ["//visibility:public"],
)


proto_library(
  name = "lp_hmi_config_proto",
  srcs = ["lp_hmi_config.proto"],
  deps = [":lp_common_proto", ":lp_hmi_display_proto", ":basic_common_proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)


cc_proto_library(
  name = "lp_hmi_config_proto_cc",
  deps = [":lp_hmi_config_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_hmi_config_proto_py",
  protos = [":lp_hmi_config_proto"],
  visibility = ["//visibility:public"],
)

proto_library(
  name = "lp_voice_control_input_proto",
  srcs = ["lp_voice_control_input.proto"],
  deps = [":basic_common_proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)

cc_proto_library(
  name = "lp_voice_control_input_proto_cc",
  deps = [":lp_voice_control_input_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_voice_control_input_proto_py",
  protos = [":lp_voice_control_input_proto"],
  visibility = ["//visibility:public"],
)

proto_library(
  name = "lp_voice_control_output_proto",
  srcs = ["lp_voice_control_output.proto"],
  deps = [":basic_common_proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)

cc_proto_library(
  name = "lp_voice_control_output_proto_cc",
  deps = [":lp_voice_control_output_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_voice_control_output_proto_py",
  protos = [":lp_voice_control_output_proto"],
  visibility = ["//visibility:public"],
)

proto_library(
  name = "lp_adas_health_proto",
  srcs = ["lp_adas_health.proto"],
  deps = [":basic_common_proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)

cc_proto_library(
  name = "lp_adas_health_proto_cc",
  deps = [":lp_adas_health_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_adas_health_proto_py",
  protos = [":lp_adas_health_proto"],
  visibility = ["//visibility:public"],
)

proto_library(
  name = "lp_adas_states_proto",
  srcs = ["lp_adas_states.proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)

cc_proto_library(
  name = "lp_adas_states_proto_cc",
  deps = [":lp_adas_states_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_adas_states_proto_py",
  protos = [":lp_adas_states_proto"],
  visibility = ["//visibility:public"],
)

proto_library(
  name = "lp_perception_light_proto",
  srcs = ["lp_perception_light.proto"],
  deps = [":basic_common_proto"],
  strip_import_prefix = "/proto/",
  visibility = ["//visibility:public"],
)

cc_proto_library(
  name = "lp_perception_light_proto_cc",
  deps = [":lp_perception_light_proto"],
  visibility = ["//visibility:public"],
)

python_proto_library(
  name = "lp_perception_light_proto_py",
  protos = [":lp_perception_light_proto"],
  visibility = ["//visibility:public"],
)
