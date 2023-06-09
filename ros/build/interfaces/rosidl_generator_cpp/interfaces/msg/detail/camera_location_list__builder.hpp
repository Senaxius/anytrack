// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/CameraLocationList.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__CAMERA_LOCATION_LIST__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__CAMERA_LOCATION_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/camera_location_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_CameraLocationList_locations
{
public:
  Init_CameraLocationList_locations()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::msg::CameraLocationList locations(::interfaces::msg::CameraLocationList::_locations_type arg)
  {
    msg_.locations = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::CameraLocationList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::CameraLocationList>()
{
  return interfaces::msg::builder::Init_CameraLocationList_locations();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__CAMERA_LOCATION_LIST__BUILDER_HPP_
