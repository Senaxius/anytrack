// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from scanner_interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__STRUCT_H_
#define SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__STRUCT_H_

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
#include "scanner_interfaces/msg/detail/location__struct.h"

/// Struct defined in msg/CameraLocations in the package scanner_interfaces.
/**
  * array of multiple camera locations
 */
typedef struct scanner_interfaces__msg__CameraLocations
{
  scanner_interfaces__msg__Location__Sequence locations;
} scanner_interfaces__msg__CameraLocations;

// Struct for a sequence of scanner_interfaces__msg__CameraLocations.
typedef struct scanner_interfaces__msg__CameraLocations__Sequence
{
  scanner_interfaces__msg__CameraLocations * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} scanner_interfaces__msg__CameraLocations__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SCANNER_INTERFACES__MSG__DETAIL__CAMERA_LOCATIONS__STRUCT_H_
