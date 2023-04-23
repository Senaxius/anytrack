// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from scanner_interfaces:msg/CameraXY.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__TRAITS_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "scanner_interfaces/msg/detail/camera_xy__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace scanner_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CameraXY & msg,
  std::ostream & out)
{
  out << "{";
  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: x_max
  {
    out << "x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.x_max, out);
    out << ", ";
  }

  // member: y_max
  {
    out << "y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.y_max, out);
    out << ", ";
  }

  // member: found
  {
    out << "found: ";
    rosidl_generator_traits::value_to_yaml(msg.found, out);
    out << ", ";
  }

  // member: fps
  {
    out << "fps: ";
    rosidl_generator_traits::value_to_yaml(msg.fps, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CameraXY & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: x_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x_max: ";
    rosidl_generator_traits::value_to_yaml(msg.x_max, out);
    out << "\n";
  }

  // member: y_max
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y_max: ";
    rosidl_generator_traits::value_to_yaml(msg.y_max, out);
    out << "\n";
  }

  // member: found
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "found: ";
    rosidl_generator_traits::value_to_yaml(msg.found, out);
    out << "\n";
  }

  // member: fps
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fps: ";
    rosidl_generator_traits::value_to_yaml(msg.fps, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CameraXY & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace scanner_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use scanner_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const scanner_interfaces::msg::CameraXY & msg,
  std::ostream & out, size_t indentation = 0)
{
  scanner_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use scanner_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const scanner_interfaces::msg::CameraXY & msg)
{
  return scanner_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<scanner_interfaces::msg::CameraXY>()
{
  return "scanner_interfaces::msg::CameraXY";
}

template<>
inline const char * name<scanner_interfaces::msg::CameraXY>()
{
  return "scanner_interfaces/msg/CameraXY";
}

template<>
struct has_fixed_size<scanner_interfaces::msg::CameraXY>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<scanner_interfaces::msg::CameraXY>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<scanner_interfaces::msg::CameraXY>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__TRAITS_HPP_
