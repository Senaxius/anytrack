// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from scanner_interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "scanner_interfaces/msg/detail/camera_locations__rosidl_typesupport_introspection_c.h"
#include "scanner_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "scanner_interfaces/msg/detail/camera_locations__functions.h"
#include "scanner_interfaces/msg/detail/camera_locations__struct.h"


// Include directives for member types
// Member `locations`
#include "scanner_interfaces/msg/location.h"
// Member `locations`
#include "scanner_interfaces/msg/detail/location__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  scanner_interfaces__msg__CameraLocations__init(message_memory);
}

void scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_fini_function(void * message_memory)
{
  scanner_interfaces__msg__CameraLocations__fini(message_memory);
}

size_t scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__size_function__CameraLocations__locations(
  const void * untyped_member)
{
  const scanner_interfaces__msg__Location__Sequence * member =
    (const scanner_interfaces__msg__Location__Sequence *)(untyped_member);
  return member->size;
}

const void * scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__get_const_function__CameraLocations__locations(
  const void * untyped_member, size_t index)
{
  const scanner_interfaces__msg__Location__Sequence * member =
    (const scanner_interfaces__msg__Location__Sequence *)(untyped_member);
  return &member->data[index];
}

void * scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__get_function__CameraLocations__locations(
  void * untyped_member, size_t index)
{
  scanner_interfaces__msg__Location__Sequence * member =
    (scanner_interfaces__msg__Location__Sequence *)(untyped_member);
  return &member->data[index];
}

void scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__fetch_function__CameraLocations__locations(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const scanner_interfaces__msg__Location * item =
    ((const scanner_interfaces__msg__Location *)
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__get_const_function__CameraLocations__locations(untyped_member, index));
  scanner_interfaces__msg__Location * value =
    (scanner_interfaces__msg__Location *)(untyped_value);
  *value = *item;
}

void scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__assign_function__CameraLocations__locations(
  void * untyped_member, size_t index, const void * untyped_value)
{
  scanner_interfaces__msg__Location * item =
    ((scanner_interfaces__msg__Location *)
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__get_function__CameraLocations__locations(untyped_member, index));
  const scanner_interfaces__msg__Location * value =
    (const scanner_interfaces__msg__Location *)(untyped_value);
  *item = *value;
}

bool scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__resize_function__CameraLocations__locations(
  void * untyped_member, size_t size)
{
  scanner_interfaces__msg__Location__Sequence * member =
    (scanner_interfaces__msg__Location__Sequence *)(untyped_member);
  scanner_interfaces__msg__Location__Sequence__fini(member);
  return scanner_interfaces__msg__Location__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_member_array[1] = {
  {
    "locations",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__CameraLocations, locations),  // bytes offset in struct
    NULL,  // default value
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__size_function__CameraLocations__locations,  // size() function pointer
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__get_const_function__CameraLocations__locations,  // get_const(index) function pointer
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__get_function__CameraLocations__locations,  // get(index) function pointer
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__fetch_function__CameraLocations__locations,  // fetch(index, &value) function pointer
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__assign_function__CameraLocations__locations,  // assign(index, value) function pointer
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__resize_function__CameraLocations__locations  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_members = {
  "scanner_interfaces__msg",  // message namespace
  "CameraLocations",  // message name
  1,  // number of fields
  sizeof(scanner_interfaces__msg__CameraLocations),
  scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_member_array,  // message members
  scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_init_function,  // function to initialize message memory (memory has to be allocated)
  scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_type_support_handle = {
  0,
  &scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_scanner_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, scanner_interfaces, msg, CameraLocations)() {
  scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, scanner_interfaces, msg, Location)();
  if (!scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_type_support_handle.typesupport_identifier) {
    scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &scanner_interfaces__msg__CameraLocations__rosidl_typesupport_introspection_c__CameraLocations_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
