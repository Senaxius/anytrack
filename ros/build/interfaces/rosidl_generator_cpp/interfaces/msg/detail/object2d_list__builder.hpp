// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Object2dList.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__OBJECT2D_LIST__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__OBJECT2D_LIST__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/object2d_list__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Object2dList_tracks
{
public:
  explicit Init_Object2dList_tracks(::interfaces::msg::Object2dList & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Object2dList tracks(::interfaces::msg::Object2dList::_tracks_type arg)
  {
    msg_.tracks = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Object2dList msg_;
};

class Init_Object2dList_header
{
public:
  Init_Object2dList_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Object2dList_tracks header(::interfaces::msg::Object2dList::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Object2dList_tracks(msg_);
  }

private:
  ::interfaces::msg::Object2dList msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Object2dList>()
{
  return interfaces::msg::builder::Init_Object2dList_header();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__OBJECT2D_LIST__BUILDER_HPP_
