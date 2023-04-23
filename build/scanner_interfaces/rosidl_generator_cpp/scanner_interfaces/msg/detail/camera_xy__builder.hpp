// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from scanner_interfaces:msg/CameraXY.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__BUILDER_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "scanner_interfaces/msg/detail/camera_xy__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace scanner_interfaces
{

namespace msg
{

namespace builder
{

class Init_CameraXY_fps
{
public:
  explicit Init_CameraXY_fps(::scanner_interfaces::msg::CameraXY & msg)
  : msg_(msg)
  {}
  ::scanner_interfaces::msg::CameraXY fps(::scanner_interfaces::msg::CameraXY::_fps_type arg)
  {
    msg_.fps = std::move(arg);
    return std::move(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraXY msg_;
};

class Init_CameraXY_found
{
public:
  explicit Init_CameraXY_found(::scanner_interfaces::msg::CameraXY & msg)
  : msg_(msg)
  {}
  Init_CameraXY_fps found(::scanner_interfaces::msg::CameraXY::_found_type arg)
  {
    msg_.found = std::move(arg);
    return Init_CameraXY_fps(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraXY msg_;
};

class Init_CameraXY_y_max
{
public:
  explicit Init_CameraXY_y_max(::scanner_interfaces::msg::CameraXY & msg)
  : msg_(msg)
  {}
  Init_CameraXY_found y_max(::scanner_interfaces::msg::CameraXY::_y_max_type arg)
  {
    msg_.y_max = std::move(arg);
    return Init_CameraXY_found(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraXY msg_;
};

class Init_CameraXY_x_max
{
public:
  explicit Init_CameraXY_x_max(::scanner_interfaces::msg::CameraXY & msg)
  : msg_(msg)
  {}
  Init_CameraXY_y_max x_max(::scanner_interfaces::msg::CameraXY::_x_max_type arg)
  {
    msg_.x_max = std::move(arg);
    return Init_CameraXY_y_max(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraXY msg_;
};

class Init_CameraXY_y
{
public:
  explicit Init_CameraXY_y(::scanner_interfaces::msg::CameraXY & msg)
  : msg_(msg)
  {}
  Init_CameraXY_x_max y(::scanner_interfaces::msg::CameraXY::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_CameraXY_x_max(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraXY msg_;
};

class Init_CameraXY_x
{
public:
  Init_CameraXY_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CameraXY_y x(::scanner_interfaces::msg::CameraXY::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_CameraXY_y(msg_);
  }

private:
  ::scanner_interfaces::msg::CameraXY msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::scanner_interfaces::msg::CameraXY>()
{
  return scanner_interfaces::msg::builder::Init_CameraXY_x();
}

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__BUILDER_HPP_
