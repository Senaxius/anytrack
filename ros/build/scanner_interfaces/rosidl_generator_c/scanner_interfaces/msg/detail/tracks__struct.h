// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from scanner_interfaces:msg/Tracks.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__TRACKS__STRUCT_H_
#define SCANNER_INTERFACES__MSG__DETAIL__TRACKS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'tracks'
#include "scanner_interfaces/msg/detail/object__struct.h"

/// Struct defined in msg/Tracks in the package scanner_interfaces.
/**
  * array of multiple tracked objects
 */
typedef struct scanner_interfaces__msg__Tracks
{
  std_msgs__msg__Header header;
  scanner_interfaces__msg__Object__Sequence tracks;
} scanner_interfaces__msg__Tracks;

// Struct for a sequence of scanner_interfaces__msg__Tracks.
typedef struct scanner_interfaces__msg__Tracks__Sequence
{
  scanner_interfaces__msg__Tracks * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} scanner_interfaces__msg__Tracks__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SCANNER_INTERFACES__MSG__DETAIL__TRACKS__STRUCT_H_
