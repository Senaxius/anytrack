// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from scanner_interfaces:msg/Location.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__LOCATION__STRUCT_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__LOCATION__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__scanner_interfaces__msg__Location __attribute__((deprecated))
#else
# define DEPRECATED__scanner_interfaces__msg__Location __declspec(deprecated)
#endif

namespace scanner_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Location_
{
  using Type = Location_<ContainerAllocator>;

  explicit Location_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0;
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->ax = 0.0;
      this->ay = 0.0;
      this->az = 0.0;
    }
  }

  explicit Location_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0;
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->ax = 0.0;
      this->ay = 0.0;
      this->az = 0.0;
    }
  }

  // field types and members
  using _id_type =
    int8_t;
  _id_type id;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _z_type =
    double;
  _z_type z;
  using _ax_type =
    double;
  _ax_type ax;
  using _ay_type =
    double;
  _ay_type ay;
  using _az_type =
    double;
  _az_type az;

  // setters for named parameter idiom
  Type & set__id(
    const int8_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const double & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__ax(
    const double & _arg)
  {
    this->ax = _arg;
    return *this;
  }
  Type & set__ay(
    const double & _arg)
  {
    this->ay = _arg;
    return *this;
  }
  Type & set__az(
    const double & _arg)
  {
    this->az = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    scanner_interfaces::msg::Location_<ContainerAllocator> *;
  using ConstRawPtr =
    const scanner_interfaces::msg::Location_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<scanner_interfaces::msg::Location_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<scanner_interfaces::msg::Location_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::Location_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::Location_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::Location_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::Location_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<scanner_interfaces::msg::Location_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<scanner_interfaces::msg::Location_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__scanner_interfaces__msg__Location
    std::shared_ptr<scanner_interfaces::msg::Location_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__scanner_interfaces__msg__Location
    std::shared_ptr<scanner_interfaces::msg::Location_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Location_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->ax != other.ax) {
      return false;
    }
    if (this->ay != other.ay) {
      return false;
    }
    if (this->az != other.az) {
      return false;
    }
    return true;
  }
  bool operator!=(const Location_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Location_

// alias to use template instance with default allocator
using Location =
  scanner_interfaces::msg::Location_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__LOCATION__STRUCT_HPP_
