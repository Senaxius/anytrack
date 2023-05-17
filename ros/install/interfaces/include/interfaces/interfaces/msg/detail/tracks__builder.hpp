// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Tracks.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__TRACKS__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__TRACKS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interfaces/msg/detail/tracks__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Tracks_tracks
{
public:
  explicit Init_Tracks_tracks(::interfaces::msg::Tracks & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Tracks tracks(::interfaces::msg::Tracks::_tracks_type arg)
  {
    msg_.tracks = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Tracks msg_;
};

class Init_Tracks_header
{
public:
  Init_Tracks_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Tracks_tracks header(::interfaces::msg::Tracks::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Tracks_tracks(msg_);
  }

private:
  ::interfaces::msg::Tracks msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Tracks>()
{
  return interfaces::msg::builder::Init_Tracks_header();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__TRACKS__BUILDER_HPP_
