// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from scanner_interfaces:msg/Tracks.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "scanner_interfaces/msg/detail/tracks__rosidl_typesupport_introspection_c.h"
#include "scanner_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "scanner_interfaces/msg/detail/tracks__functions.h"
#include "scanner_interfaces/msg/detail/tracks__struct.h"


// Include directives for member types
// Member `tracks`
#include "scanner_interfaces/msg/object.h"
// Member `tracks`
#include "scanner_interfaces/msg/detail/object__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  scanner_interfaces__msg__Tracks__init(message_memory);
}

void scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_fini_function(void * message_memory)
{
  scanner_interfaces__msg__Tracks__fini(message_memory);
}

size_t scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__size_function__Tracks__tracks(
  const void * untyped_member)
{
  const scanner_interfaces__msg__Object__Sequence * member =
    (const scanner_interfaces__msg__Object__Sequence *)(untyped_member);
  return member->size;
}

const void * scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__get_const_function__Tracks__tracks(
  const void * untyped_member, size_t index)
{
  const scanner_interfaces__msg__Object__Sequence * member =
    (const scanner_interfaces__msg__Object__Sequence *)(untyped_member);
  return &member->data[index];
}

void * scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__get_function__Tracks__tracks(
  void * untyped_member, size_t index)
{
  scanner_interfaces__msg__Object__Sequence * member =
    (scanner_interfaces__msg__Object__Sequence *)(untyped_member);
  return &member->data[index];
}

void scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__fetch_function__Tracks__tracks(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const scanner_interfaces__msg__Object * item =
    ((const scanner_interfaces__msg__Object *)
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__get_const_function__Tracks__tracks(untyped_member, index));
  scanner_interfaces__msg__Object * value =
    (scanner_interfaces__msg__Object *)(untyped_value);
  *value = *item;
}

void scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__assign_function__Tracks__tracks(
  void * untyped_member, size_t index, const void * untyped_value)
{
  scanner_interfaces__msg__Object * item =
    ((scanner_interfaces__msg__Object *)
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__get_function__Tracks__tracks(untyped_member, index));
  const scanner_interfaces__msg__Object * value =
    (const scanner_interfaces__msg__Object *)(untyped_value);
  *item = *value;
}

bool scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__resize_function__Tracks__tracks(
  void * untyped_member, size_t size)
{
  scanner_interfaces__msg__Object__Sequence * member =
    (scanner_interfaces__msg__Object__Sequence *)(untyped_member);
  scanner_interfaces__msg__Object__Sequence__fini(member);
  return scanner_interfaces__msg__Object__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_member_array[1] = {
  {
    "tracks",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(scanner_interfaces__msg__Tracks, tracks),  // bytes offset in struct
    NULL,  // default value
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__size_function__Tracks__tracks,  // size() function pointer
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__get_const_function__Tracks__tracks,  // get_const(index) function pointer
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__get_function__Tracks__tracks,  // get(index) function pointer
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__fetch_function__Tracks__tracks,  // fetch(index, &value) function pointer
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__assign_function__Tracks__tracks,  // assign(index, value) function pointer
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__resize_function__Tracks__tracks  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_members = {
  "scanner_interfaces__msg",  // message namespace
  "Tracks",  // message name
  1,  // number of fields
  sizeof(scanner_interfaces__msg__Tracks),
  scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_member_array,  // message members
  scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_init_function,  // function to initialize message memory (memory has to be allocated)
  scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_type_support_handle = {
  0,
  &scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_scanner_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, scanner_interfaces, msg, Tracks)() {
  scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, scanner_interfaces, msg, Object)();
  if (!scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_type_support_handle.typesupport_identifier) {
    scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &scanner_interfaces__msg__Tracks__rosidl_typesupport_introspection_c__Tracks_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
