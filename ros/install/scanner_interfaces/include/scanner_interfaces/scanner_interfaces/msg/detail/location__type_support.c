// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from scanner_interfaces:msg/Location.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "scanner_interfaces/msg/detail/location__rosidl_typesupport_introspection_c.h"
#include "scanner_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "scanner_interfaces/msg/detail/location__functions.h"
#include "scanner_interfaces/msg/detail/location__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  scanner_interfaces__msg__Location__init(message_memory);
}

void scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_fini_function(void * message_memory)
{
  scanner_interfaces__msg__Location__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_member_array[7] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT8,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "ax",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, ax),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "ay",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, ay),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "az",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Location, az),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_members = {
  "scanner_interfaces__msg",  // message namespace
  "Location",  // message name
  7,  // number of fields
  sizeof(scanner_interfaces__msg__Location),
  scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_member_array,  // message members
  scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_init_function,  // function to initialize message memory (memory has to be allocated)
  scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_type_support_handle = {
  0,
  &scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_scanner_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, scanner_interfaces, msg, Location)() {
  if (!scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_type_support_handle.typesupport_identifier) {
    scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &scanner_interfaces__msg__Location__rosidl_typesupport_introspection_c__Location_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
