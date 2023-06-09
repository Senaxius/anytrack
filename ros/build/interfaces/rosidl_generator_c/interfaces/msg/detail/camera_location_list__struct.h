// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/CameraLocationList.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__CAMERA_LOCATION_LIST__STRUCT_H_
#define INTERFACES__MSG__DETAIL__CAMERA_LOCATION_LIST__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'locations'
#include "interfaces/msg/detail/camera_location__struct.h"

/// Struct defined in msg/CameraLocationList in the package interfaces.
/**
  * array of multiple camera locations
 */
typedef struct interfaces__msg__CameraLocationList
{
  interfaces__msg__CameraLocation__Sequence locations;
} interfaces__msg__CameraLocationList;

// Struct for a sequence of interfaces__msg__CameraLocationList.
typedef struct interfaces__msg__CameraLocationList__Sequence
{
  interfaces__msg__CameraLocationList * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__CameraLocationList__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__CAMERA_LOCATION_LIST__STRUCT_H_
