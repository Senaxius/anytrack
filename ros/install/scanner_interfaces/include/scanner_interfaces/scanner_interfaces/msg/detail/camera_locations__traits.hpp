// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from scanner_interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__TRAITS_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "scanner_interfaces/msg/detail/camera_locations__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'locations'
#include "scanner_interfaces/msg/detail/location__traits.hpp"

namespace scanner_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const CameraLocations & msg,
  std::ostream & out)
{
  out << "{";
  // member: locations
  {
    if (msg.locations.size() == 0) {
      out << "locations: []";
    } else {
      out << "locations: [";
      size_t pending_items = msg.locations.size();
      for (auto item : msg.locations) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CameraLocations & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: locations
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.locations.size() == 0) {
      out << "locations: []\n";
    } else {
      out << "locations:\n";
      for (auto item : msg.locations) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CameraLocations & msg, bool use_flow_style = false)
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
  const scanner_interfaces::msg::CameraLocations & msg,
  std::ostream & out, size_t indentation = 0)
{
  scanner_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use scanner_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const scanner_interfaces::msg::CameraLocations & msg)
{
  return scanner_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<scanner_interfaces::msg::CameraLocations>()
{
  return "scanner_interfaces::msg::CameraLocations";
}

template<>
inline const char * name<scanner_interfaces::msg::CameraLocations>()
{
  return "scanner_interfaces/msg/CameraLocations";
}

template<>
struct has_fixed_size<scanner_interfaces::msg::CameraLocations>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<scanner_interfaces::msg::CameraLocations>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<scanner_interfaces::msg::CameraLocations>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__TRAITS_HPP_
