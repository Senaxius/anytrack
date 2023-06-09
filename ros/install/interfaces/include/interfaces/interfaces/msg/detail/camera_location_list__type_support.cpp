// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from interfaces:msg/CameraLocationList.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "interfaces/msg/detail/camera_location_list__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void CameraLocationList_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) interfaces::msg::CameraLocationList(_init);
}

void CameraLocationList_fini_function(void * message_memory)
{
  auto typed_message = static_cast<interfaces::msg::CameraLocationList *>(message_memory);
  typed_message->~CameraLocationList();
}

size_t size_function__CameraLocationList__locations(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<interfaces::msg::CameraLocation> *>(untyped_member);
  return member->size();
}

const void * get_const_function__CameraLocationList__locations(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<interfaces::msg::CameraLocation> *>(untyped_member);
  return &member[index];
}

void * get_function__CameraLocationList__locations(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<interfaces::msg::CameraLocation> *>(untyped_member);
  return &member[index];
}

void fetch_function__CameraLocationList__locations(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const interfaces::msg::CameraLocation *>(
    get_const_function__CameraLocationList__locations(untyped_member, index));
  auto & value = *reinterpret_cast<interfaces::msg::CameraLocation *>(untyped_value);
  value = item;
}

void assign_function__CameraLocationList__locations(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<interfaces::msg::CameraLocation *>(
    get_function__CameraLocationList__locations(untyped_member, index));
  const auto & value = *reinterpret_cast<const interfaces::msg::CameraLocation *>(untyped_value);
  item = value;
}

void resize_function__CameraLocationList__locations(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<interfaces::msg::CameraLocation> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember CameraLocationList_message_member_array[1] = {
  {
    "locations",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<interfaces::msg::CameraLocation>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces::msg::CameraLocationList, locations),  // bytes offset in struct
    nullptr,  // default value
    size_function__CameraLocationList__locations,  // size() function pointer
    get_const_function__CameraLocationList__locations,  // get_const(index) function pointer
    get_function__CameraLocationList__locations,  // get(index) function pointer
    fetch_function__CameraLocationList__locations,  // fetch(index, &value) function pointer
    assign_function__CameraLocationList__locations,  // assign(index, value) function pointer
    resize_function__CameraLocationList__locations  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers CameraLocationList_message_members = {
  "interfaces::msg",  // message namespace
  "CameraLocationList",  // message name
  1,  // number of fields
  sizeof(interfaces::msg::CameraLocationList),
  CameraLocationList_message_member_array,  // message members
  CameraLocationList_init_function,  // function to initialize message memory (memory has to be allocated)
  CameraLocationList_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t CameraLocationList_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &CameraLocationList_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<interfaces::msg::CameraLocationList>()
{
  return &::interfaces::msg::rosidl_typesupport_introspection_cpp::CameraLocationList_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, interfaces, msg, CameraLocationList)() {
  return &::interfaces::msg::rosidl_typesupport_introspection_cpp::CameraLocationList_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
