// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from scanner_interfaces:msg/CameraXY.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__STRUCT_H_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/CameraXY in the package scanner_interfaces.
typedef struct scanner_interfaces__msg__CameraXY
{
  double x;
  double y;
  int64_t x_max;
  int64_t y_max;
  bool found;
} scanner_interfaces__msg__CameraXY;

// Struct for a sequence of scanner_interfaces__msg__CameraXY.
typedef struct scanner_interfaces__msg__CameraXY__Sequence
{
  scanner_interfaces__msg__CameraXY * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} scanner_interfaces__msg__CameraXY__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_XY__STRUCT_H_
