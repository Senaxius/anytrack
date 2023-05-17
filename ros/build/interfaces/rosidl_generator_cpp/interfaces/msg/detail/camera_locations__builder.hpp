// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/camera_locations__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_CameraLocations_locations
{
public:
  Init_CameraLocations_locations()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::msg::CameraLocations locations(::interfaces::msg::CameraLocations::_locations_type arg)
  {
    msg_.locations = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::CameraLocations msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::CameraLocations>()
{
  return interfaces::msg::builder::Init_CameraLocations_locations();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__BUILDER_HPP_
