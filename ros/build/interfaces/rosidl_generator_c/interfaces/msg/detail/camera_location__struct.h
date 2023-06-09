// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/CameraLocation.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__CAMERA_LOCATION__STRUCT_H_
#define INTERFACES__MSG__DETAIL__CAMERA_LOCATION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/CameraLocation in the package interfaces.
/**
  * characteristics of a camera
 */
typedef struct interfaces__msg__CameraLocation
{
  int8_t id;
  double x;
  double y;
  double z;
  double ax;
  double ay;
  double az;
} interfaces__msg__CameraLocation;

// Struct for a sequence of interfaces__msg__CameraLocation.
typedef struct interfaces__msg__CameraLocation__Sequence
{
  interfaces__msg__CameraLocation * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__CameraLocation__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__CAMERA_LOCATION__STRUCT_H_
