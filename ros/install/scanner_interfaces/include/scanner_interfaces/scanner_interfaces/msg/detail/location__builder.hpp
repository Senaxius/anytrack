// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from scanner_interfaces:msg/Location.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__LOCATION__BUILDER_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__LOCATION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "scanner_interfaces/msg/detail/location__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace scanner_interfaces
{

namespace msg
{

namespace builder
{

class Init_Location_az
{
public:
  explicit Init_Location_az(::scanner_interfaces::msg::Location & msg)
  : msg_(msg)
  {}
  ::scanner_interfaces::msg::Location az(::scanner_interfaces::msg::Location::_az_type arg)
  {
    msg_.az = std::move(arg);
    return std::move(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

class Init_Location_ay
{
public:
  explicit Init_Location_ay(::scanner_interfaces::msg::Location & msg)
  : msg_(msg)
  {}
  Init_Location_az ay(::scanner_interfaces::msg::Location::_ay_type arg)
  {
    msg_.ay = std::move(arg);
    return Init_Location_az(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

class Init_Location_ax
{
public:
  explicit Init_Location_ax(::scanner_interfaces::msg::Location & msg)
  : msg_(msg)
  {}
  Init_Location_ay ax(::scanner_interfaces::msg::Location::_ax_type arg)
  {
    msg_.ax = std::move(arg);
    return Init_Location_ay(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

class Init_Location_z
{
public:
  explicit Init_Location_z(::scanner_interfaces::msg::Location & msg)
  : msg_(msg)
  {}
  Init_Location_ax z(::scanner_interfaces::msg::Location::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_Location_ax(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

class Init_Location_y
{
public:
  explicit Init_Location_y(::scanner_interfaces::msg::Location & msg)
  : msg_(msg)
  {}
  Init_Location_z y(::scanner_interfaces::msg::Location::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Location_z(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

class Init_Location_x
{
public:
  explicit Init_Location_x(::scanner_interfaces::msg::Location & msg)
  : msg_(msg)
  {}
  Init_Location_y x(::scanner_interfaces::msg::Location::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Location_y(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

class Init_Location_id
{
public:
  Init_Location_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Location_x id(::scanner_interfaces::msg::Location::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Location_x(msg_);
  }

private:
  ::scanner_interfaces::msg::Location msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::scanner_interfaces::msg::Location>()
{
  return scanner_interfaces::msg::builder::Init_Location_id();
}

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__LOCATION__BUILDER_HPP_
