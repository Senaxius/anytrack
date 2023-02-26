// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from scanner_interfaces:msg/Object.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__OBJECT__BUILDER_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "scanner_interfaces/msg/detail/object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace scanner_interfaces
{

namespace msg
{

namespace builder
{

class Init_Object_diff
{
public:
  explicit Init_Object_diff(::scanner_interfaces::msg::Object & msg)
  : msg_(msg)
  {}
  ::scanner_interfaces::msg::Object diff(::scanner_interfaces::msg::Object::_diff_type arg)
  {
    msg_.diff = std::move(arg);
    return std::move(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

class Init_Object_radius
{
public:
  explicit Init_Object_radius(::scanner_interfaces::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_diff radius(::scanner_interfaces::msg::Object::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return Init_Object_diff(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

class Init_Object_y_max
{
public:
  explicit Init_Object_y_max(::scanner_interfaces::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_radius y_max(::scanner_interfaces::msg::Object::_y_max_type arg)
  {
    msg_.y_max = std::move(arg);
    return Init_Object_radius(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

class Init_Object_x_max
{
public:
  explicit Init_Object_x_max(::scanner_interfaces::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_y_max x_max(::scanner_interfaces::msg::Object::_x_max_type arg)
  {
    msg_.x_max = std::move(arg);
    return Init_Object_y_max(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

class Init_Object_y
{
public:
  explicit Init_Object_y(::scanner_interfaces::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_x_max y(::scanner_interfaces::msg::Object::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Object_x_max(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

class Init_Object_x
{
public:
  explicit Init_Object_x(::scanner_interfaces::msg::Object & msg)
  : msg_(msg)
  {}
  Init_Object_y x(::scanner_interfaces::msg::Object::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Object_y(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

class Init_Object_id
{
public:
  Init_Object_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Object_x id(::scanner_interfaces::msg::Object::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Object_x(msg_);
  }

private:
  ::scanner_interfaces::msg::Object msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::scanner_interfaces::msg::Object>()
{
  return scanner_interfaces::msg::builder::Init_Object_id();
}

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__OBJECT__BUILDER_HPP_
