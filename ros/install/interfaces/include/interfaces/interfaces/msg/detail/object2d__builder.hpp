// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Object2d.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__OBJECT2D__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__OBJECT2D__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/object2d__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Object2d_diff
{
public:
  explicit Init_Object2d_diff(::interfaces::msg::Object2d & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Object2d diff(::interfaces::msg::Object2d::_diff_type arg)
  {
    msg_.diff = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

class Init_Object2d_radius
{
public:
  explicit Init_Object2d_radius(::interfaces::msg::Object2d & msg)
  : msg_(msg)
  {}
  Init_Object2d_diff radius(::interfaces::msg::Object2d::_radius_type arg)
  {
    msg_.radius = std::move(arg);
    return Init_Object2d_diff(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

class Init_Object2d_y_max
{
public:
  explicit Init_Object2d_y_max(::interfaces::msg::Object2d & msg)
  : msg_(msg)
  {}
  Init_Object2d_radius y_max(::interfaces::msg::Object2d::_y_max_type arg)
  {
    msg_.y_max = std::move(arg);
    return Init_Object2d_radius(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

class Init_Object2d_x_max
{
public:
  explicit Init_Object2d_x_max(::interfaces::msg::Object2d & msg)
  : msg_(msg)
  {}
  Init_Object2d_y_max x_max(::interfaces::msg::Object2d::_x_max_type arg)
  {
    msg_.x_max = std::move(arg);
    return Init_Object2d_y_max(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

class Init_Object2d_y
{
public:
  explicit Init_Object2d_y(::interfaces::msg::Object2d & msg)
  : msg_(msg)
  {}
  Init_Object2d_x_max y(::interfaces::msg::Object2d::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Object2d_x_max(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

class Init_Object2d_x
{
public:
  explicit Init_Object2d_x(::interfaces::msg::Object2d & msg)
  : msg_(msg)
  {}
  Init_Object2d_y x(::interfaces::msg::Object2d::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Object2d_y(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

class Init_Object2d_id
{
public:
  Init_Object2d_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Object2d_x id(::interfaces::msg::Object2d::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_Object2d_x(msg_);
  }

private:
  ::interfaces::msg::Object2d msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Object2d>()
{
  return interfaces::msg::builder::Init_Object2d_id();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__OBJECT2D__BUILDER_HPP_
