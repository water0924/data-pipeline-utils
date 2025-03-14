project(common-protocol)

set(M_VERSION_MAJOR 2)
set(M_VERSION_MINOR 0)
set(M_VERSION_PATCH 26)
set(M_VERSION ${M_VERSION_MAJOR}.${M_VERSION_MINOR}.${M_VERSION_PATCH})

set(PROTO_GENERATE_PATH ${REPO_ROOT_PATH}/proto_gen)

# Generate cpp/python files using macro from CMake>=3.15.0.
set(PROTOBUF_GENERATE_CPP_APPEND_PATH FALSE)
# Use PROTOBUF_IMPORT_DIRS to set both import and export dir for protobuf.
set(PROTOBUF_IMPORT_DIRS ${CMAKE_CURRENT_SOURCE_DIR} PROTOC_OUT_DIR
                         ${PROTO_GENERATE_PATH})

set(PROTOS)
if (COMMON_PROTO_INCLUDE_FOLDERS)
    foreach(folder ${COMMON_PROTO_INCLUDE_FOLDERS})
        file(GLOB_RECURSE module_protos ${CMAKE_CURRENT_SOURCE_DIR}/${folder}/*.proto)
        list(APPEND PROTOS "${module_protos}")
    endforeach()
else()
    # glob all if not specified
    file(GLOB_RECURSE PROTOS *.proto)
    message(STATUS "COMMON_PROTO_INCLUDE_FOLDERS not set or empty, build all protos")
endif()
foreach(PROTO_PATH ${PROTOS})
  string(FIND ${PROTO_PATH} "${CMAKE_CURRENT_SOURCE_DIR}/church"
              IS_CHURCH_PROTO)
  if(NOT ${IS_CHURCH_PROTO} EQUAL -1)
    list(REMOVE_ITEM PROTOS ${PROTO_PATH})
  endif()
endforeach(PROTO_PATH)
if (NOT PROTOS)
    message(STATUS "proto to includes: ${COMMON_PROTO_INCLUDE_FOLDERS}")
    message(STATUS "No proto files are found, just skip")
    return()
endif()

protobuf_generate_cpp(PROTO_SOURCES PROTO_HEADERS ${PROTOS})
protobuf_generate_python(PROTO_PY ${PROTOS})

file(GLOB_RECURSE CHURCH_PROTOS ${CMAKE_CURRENT_SOURCE_DIR}/church/*.proto)
protobuf_generate_cpp(CHURCH_PROTO_SOURCES CHURCH_PROTO_HEADERS
                      ${CHURCH_PROTOS})
protobuf_generate_python(CHURCH_PROTO_PY ${CHURCH_PROTOS})

# The py_target here is added only for the purpose of generating .py files using
# protobuf_generate_python and no real target will be generated.
add_custom_target(py_target ALL DEPENDS ${PROTO_PY} ${CHURCH_PROTO_PY})

# Add __init__.py for python library
file(
  GLOB_RECURSE PROTO_FILES
  RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
  *.proto)

foreach(PROTO_FILE ${PROTO_FILES})
  get_filename_component(RELATIVE_DIR ${PROTO_FILE} DIRECTORY)
  execute_process(COMMAND mkdir -p ${PROTO_GENERATE_PATH}/${RELATIVE_DIR})
  execute_process(COMMAND touch
                          ${PROTO_GENERATE_PATH}/${RELATIVE_DIR}/__init__.py)
endforeach()
execute_process(COMMAND touch ${PROTO_GENERATE_PATH}/__init__.py)

add_library(proto ${LIBRARY_TYPE} ${PROTO_SOURCES})
add_library(church_proto ${LIBRARY_TYPE} ${CHURCH_PROTO_SOURCES})

target_include_directories(
  church_proto
  PUBLIC $<BUILD_INTERFACE:${PROTO_GENERATE_PATH}>
         $<BUILD_INTERFACE:${PROTOBUF_INCLUDE_DIRS}>
         $<INSTALL_INTERFACE:include/proto>)

set_target_properties(proto PROPERTIES SOVERSION ${M_VERSION_MAJOR}
                                       VERSION ${M_VERSION})

# Specify different include directories for build time and install time.
target_include_directories(
  proto
  PUBLIC $<BUILD_INTERFACE:${PROTO_GENERATE_PATH}>
         $<BUILD_INTERFACE:${PROTOBUF_INCLUDE_DIRS}>
         $<INSTALL_INTERFACE:include/proto>)

if(DEFINED ARM_PROTOBUF_PATH)
  set(PROTOBUF_LIBRARIES ${ARM_PROTOBUF_PATH}/libprotobuf.so -lpthread)
endif()

target_link_libraries(proto PUBLIC ${PROTOBUF_LIBRARIES})

if(${USE_STATIC_LIB})

else()
  # Install libproto.so.
  install(
    TARGETS proto
    EXPORT protoTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES
    DESTINATION include/proto)

  # Install protoTargets.cmake.
  install(
    EXPORT protoTargets
    FILE protoTargets.cmake
    NAMESPACE Common::
    DESTINATION lib/cmake/proto)
endif()

# By add alias, we guarantee that using add_subdirectory and find_package
# provide the same targets and namespaces. For reference, see Daniel Pfeifer’s
# C++Now 2017 talk Effective CMake.
add_library(Common::proto ALIAS proto)

# Install header files with preserved directory structure.
install(
  DIRECTORY ${PROTO_GENERATE_PATH}/
  DESTINATION include/proto
  FILES_MATCHING
  PATTERN "*.h*")

install(
  DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/
  DESTINATION include/proto
  FILES_MATCHING
  PATTERN "*.proto")

# Install python files with preserved directory structure.
install(
  DIRECTORY ${PROTO_GENERATE_PATH}/
  DESTINATION include/proto
  FILES_MATCHING
  PATTERN "*.py*")

# Install proto-config.cmake which resolves dependency when find_package(proto).
install(FILES "${REPO_ROOT_PATH}/proto/proto-config.cmake"
        DESTINATION lib/cmake/proto)
