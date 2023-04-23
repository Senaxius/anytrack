// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from scanner_interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__STRUCT_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'locations'
#include "scanner_interfaces/msg/detail/location__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__scanner_interfaces__msg__CameraLocations __attribute__((deprecated))
#else
# define DEPRECATED__scanner_interfaces__msg__CameraLocations __declspec(deprecated)
#endif

namespace scanner_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CameraLocations_
{
  using Type = CameraLocations_<ContainerAllocator>;

  explicit CameraLocations_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit CameraLocations_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _locations_type =
    std::vector<scanner_interfaces::msg::Location_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<scanner_interfaces::msg::Location_<ContainerAllocator>>>;
  _locations_type locations;

  // setters for named parameter idiom
  Type & set__locations(
    const std::vector<scanner_interfaces::msg::Location_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<scanner_interfaces::msg::Location_<ContainerAllocator>>> & _arg)
  {
    this->locations = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    scanner_interfaces::msg::CameraLocations_<ContainerAllocator> *;
  using ConstRawPtr =
    const scanner_interfaces::msg::CameraLocations_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::CameraLocations_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::CameraLocations_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__scanner_interfaces__msg__CameraLocations
    std::shared_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__scanner_interfaces__msg__CameraLocations
    std::shared_ptr<scanner_interfaces::msg::CameraLocations_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CameraLocations_ & other) const
  {
    if (this->locations != other.locations) {
      return false;
    }
    return true;
  }
  bool operator!=(const CameraLocations_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CameraLocations_

// alias to use template instance with default allocator
using CameraLocations =
  scanner_interfaces::msg::CameraLocations_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__STRUCT_HPP_
