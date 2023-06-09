// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/Object2dList.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__OBJECT2D_LIST__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__OBJECT2D_LIST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'tracks'
#include "interfaces/msg/detail/object2d__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__interfaces__msg__Object2dList __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__Object2dList __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Object2dList_
{
  using Type = Object2dList_<ContainerAllocator>;

  explicit Object2dList_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    (void)_init;
  }

  explicit Object2dList_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _tracks_type =
    std::vector<interfaces::msg::Object2d_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<interfaces::msg::Object2d_<ContainerAllocator>>>;
  _tracks_type tracks;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__tracks(
    const std::vector<interfaces::msg::Object2d_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<interfaces::msg::Object2d_<ContainerAllocator>>> & _arg)
  {
    this->tracks = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::Object2dList_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::Object2dList_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::Object2dList_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::Object2dList_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Object2dList_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Object2dList_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Object2dList_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Object2dList_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::Object2dList_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::Object2dList_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__Object2dList
    std::shared_ptr<interfaces::msg::Object2dList_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__Object2dList
    std::shared_ptr<interfaces::msg::Object2dList_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Object2dList_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->tracks != other.tracks) {
      return false;
    }
    return true;
  }
  bool operator!=(const Object2dList_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Object2dList_

// alias to use template instance with default allocator
using Object2dList =
  interfaces::msg::Object2dList_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__OBJECT2D_LIST__STRUCT_HPP_
