// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from scanner_interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__BUILDER_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "scanner_interfaces/msg/detail/camera_locations__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace scanner_interfaces
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
  ::scanner_interfaces::msg::CameraLocations locations(::scanner_interfaces::msg::CameraLocations::_locations_type arg)
  {
    msg_.locations = std::move(arg);
    return std::move(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraLocations msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::scanner_interfaces::msg::CameraLocations>()
{
  return scanner_interfaces::msg::builder::Init_CameraLocations_locations();
}

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__BUILDER_HPP_
