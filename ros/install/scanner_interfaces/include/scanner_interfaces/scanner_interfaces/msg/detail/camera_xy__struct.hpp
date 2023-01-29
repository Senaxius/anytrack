// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from scanner_interfaces:msg/CameraXY.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__STRUCT_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__scanner_interfaces__msg__CameraXY __attribute__((deprecated))
#else
# define DEPRECATED__scanner_interfaces__msg__CameraXY __declspec(deprecated)
#endif

namespace scanner_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CameraXY_
{
  using Type = CameraXY_<ContainerAllocator>;

  explicit CameraXY_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->x_max = 0ll;
      this->y_max = 0ll;
      this->found = false;
      this->fps = 0ll;
    }
  }

  explicit CameraXY_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->x_max = 0ll;
      this->y_max = 0ll;
      this->found = false;
      this->fps = 0ll;
    }
  }

  // field types and members
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _x_max_type =
    int64_t;
  _x_max_type x_max;
  using _y_max_type =
    int64_t;
  _y_max_type y_max;
  using _found_type =
    bool;
  _found_type found;
  using _fps_type =
    int64_t;
  _fps_type fps;

  // setters for named parameter idiom
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
  Type & set__x_max(
    const int64_t & _arg)
  {
    this->x_max = _arg;
    return *this;
  }
  Type & set__y_max(
    const int64_t & _arg)
  {
    this->y_max = _arg;
    return *this;
  }
  Type & set__found(
    const bool & _arg)
  {
    this->found = _arg;
    return *this;
  }
  Type & set__fps(
    const int64_t & _arg)
  {
    this->fps = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    scanner_interfaces::msg::CameraXY_<ContainerAllocator> *;
  using ConstRawPtr =
    const scanner_interfaces::msg::CameraXY_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::CameraXY_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::CameraXY_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__scanner_interfaces__msg__CameraXY
    std::shared_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__scanner_interfaces__msg__CameraXY
    std::shared_ptr<scanner_interfaces::msg::CameraXY_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CameraXY_ & other) const
  {
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->x_max != other.x_max) {
      return false;
    }
    if (this->y_max != other.y_max) {
      return false;
    }
    if (this->found != other.found) {
      return false;
    }
    if (this->fps != other.fps) {
      return false;
    }
    return true;
  }
  bool operator!=(const CameraXY_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CameraXY_

// alias to use template instance with default allocator
using CameraXY =
  scanner_interfaces::msg::CameraXY_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__STRUCT_HPP_