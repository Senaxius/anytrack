// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/CameraLocation.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__CAMERA_LOCATION__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__CAMERA_LOCATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/camera_location__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_CameraLocation_az
{
public:
  explicit Init_CameraLocation_az(::interfaces::msg::CameraLocation & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::CameraLocation az(::interfaces::msg::CameraLocation::_az_type arg)
  {
    msg_.az = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

class Init_CameraLocation_ay
{
public:
  explicit Init_CameraLocation_ay(::interfaces::msg::CameraLocation & msg)
  : msg_(msg)
  {}
  Init_CameraLocation_az ay(::interfaces::msg::CameraLocation::_ay_type arg)
  {
    msg_.ay = std::move(arg);
    return Init_CameraLocation_az(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

class Init_CameraLocation_ax
{
public:
  explicit Init_CameraLocation_ax(::interfaces::msg::CameraLocation & msg)
  : msg_(msg)
  {}
  Init_CameraLocation_ay ax(::interfaces::msg::CameraLocation::_ax_type arg)
  {
    msg_.ax = std::move(arg);
    return Init_CameraLocation_ay(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

class Init_CameraLocation_z
{
public:
  explicit Init_CameraLocation_z(::interfaces::msg::CameraLocation & msg)
  : msg_(msg)
  {}
  Init_CameraLocation_ax z(::interfaces::msg::CameraLocation::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_CameraLocation_ax(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

class Init_CameraLocation_y
{
public:
  explicit Init_CameraLocation_y(::interfaces::msg::CameraLocation & msg)
  : msg_(msg)
  {}
  Init_CameraLocation_z y(::interfaces::msg::CameraLocation::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_CameraLocation_z(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

class Init_CameraLocation_x
{
public:
  explicit Init_CameraLocation_x(::interfaces::msg::CameraLocation & msg)
  : msg_(msg)
  {}
  Init_CameraLocation_y x(::interfaces::msg::CameraLocation::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_CameraLocation_y(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

class Init_CameraLocation_id
{
public:
  Init_CameraLocation_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CameraLocation_x id(::interfaces::msg::CameraLocation::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_CameraLocation_x(msg_);
  }

private:
  ::interfaces::msg::CameraLocation msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::CameraLocation>()
{
  return interfaces::msg::builder::Init_CameraLocation_id();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__CAMERA_LOCATION__BUILDER_HPP_
