// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from scanner_interfaces:msg/Tracks.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__TRACKS__STRUCT_HPP_
#define SCANNER_INTERFACES__MSG__DETAIL__TRACKS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'tracks'
#include "scanner_interfaces/msg/detail/object__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__scanner_interfaces__msg__Tracks __attribute__((deprecated))
#else
# define DEPRECATED__scanner_interfaces__msg__Tracks __declspec(deprecated)
#endif

namespace scanner_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Tracks_
{
  using Type = Tracks_<ContainerAllocator>;

  explicit Tracks_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit Tracks_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _tracks_type =
    std::vector<scanner_interfaces::msg::Object_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<scanner_interfaces::msg::Object_<ContainerAllocator>>>;
  _tracks_type tracks;

  // setters for named parameter idiom
  Type & set__tracks(
    const std::vector<scanner_interfaces::msg::Object_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<scanner_interfaces::msg::Object_<ContainerAllocator>>> & _arg)
  {
    this->tracks = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    scanner_interfaces::msg::Tracks_<ContainerAllocator> *;
  using ConstRawPtr =
    const scanner_interfaces::msg::Tracks_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::Tracks_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      scanner_interfaces::msg::Tracks_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__scanner_interfaces__msg__Tracks
    std::shared_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__scanner_interfaces__msg__Tracks
    std::shared_ptr<scanner_interfaces::msg::Tracks_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Tracks_ & other) const
  {
    if (this->tracks != other.tracks) {
      return false;
    }
    return true;
  }
  bool operator!=(const Tracks_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Tracks_

// alias to use template instance with default allocator
using Tracks =
  scanner_interfaces::msg::Tracks_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace scanner_interfaces

#endif  // SCANNER_INTERFACES__MSG__DETAIL__TRACKS__STRUCT_HPP_
