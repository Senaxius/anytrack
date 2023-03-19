// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from scanner_interfaces:msg/Location.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__LOCATION__TRAITS_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__LOCATION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "scanner_interfaces/msg/detail/location__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace scanner_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Location & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

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

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: ax
  {
    out << "ax: ";
    rosidl_generator_traits::value_to_yaml(msg.ax, out);
    out << ", ";
  }

  // member: ay
  {
    out << "ay: ";
    rosidl_generator_traits::value_to_yaml(msg.ay, out);
    out << ", ";
  }

  // member: az
  {
    out << "az: ";
    rosidl_generator_traits::value_to_yaml(msg.az, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Location & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

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

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: ax
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "ax: ";
    rosidl_generator_traits::value_to_yaml(msg.ax, out);
    out << "\n";
  }

  // member: ay
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "ay: ";
    rosidl_generator_traits::value_to_yaml(msg.ay, out);
    out << "\n";
  }

  // member: az
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "az: ";
    rosidl_generator_traits::value_to_yaml(msg.az, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Location & msg, bool use_flow_style = false)
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
  const scanner_interfaces::msg::Location & msg,
  std::ostream & out, size_t indentation = 0)
{
  scanner_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use scanner_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const scanner_interfaces::msg::Location & msg)
{
  return scanner_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<scanner_interfaces::msg::Location>()
{
  return "scanner_interfaces::msg::Location";
}

template<>
inline const char * name<scanner_interfaces::msg::Location>()
{
  return "scanner_interfaces/msg/Location";
}

template<>
struct has_fixed_size<scanner_interfaces::msg::Location>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<scanner_interfaces::msg::Location>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<scanner_interfaces::msg::Location>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SCANNER_INTERFACES__MSG__DETAIL__LOCATION__TRAITS_HPP_
