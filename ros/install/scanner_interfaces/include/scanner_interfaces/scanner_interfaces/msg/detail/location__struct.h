// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from scanner_interfaces:msg/Location.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__LOCATION__STRUCT_H_
#define SCANNER_INTERFACES__MSG__DETAIL__LOCATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Location in the package scanner_interfaces.
/**
  * characteristics of a camera
 */
typedef struct scanner_interfaces__msg__Location
{
  int8_t id;
  double x;
  double y;
  double z;
  double ax;
  double ay;
  double az;
} scanner_interfaces__msg__Location;

// Struct for a sequence of scanner_interfaces__msg__Location.
typedef struct scanner_interfaces__msg__Location__Sequence
{
  scanner_interfaces__msg__Location * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} scanner_interfaces__msg__Location__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SCANNER_INTERFACES__MSG__DETAIL__LOCATION__STRUCT_H_
