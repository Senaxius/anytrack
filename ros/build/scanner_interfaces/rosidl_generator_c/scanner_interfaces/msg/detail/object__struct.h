// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from scanner_interfaces:msg/Object.idl
// generated code does not contain a copyright notice

#ifndef SCANNER_INTERFACES__MSG__DETAIL__OBJECT__STRUCT_H_
#define SCANNER_INTERFACES__MSG__DETAIL__OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Object in the package scanner_interfaces.
/**
  * characteristics of a tracked object
 */
typedef struct scanner_interfaces__msg__Object
{
  int8_t id;
  double x;
  double y;
  int64_t x_max;
  int64_t y_max;
  double radius;
  int64_t diff;
} scanner_interfaces__msg__Object;

// Struct for a sequence of scanner_interfaces__msg__Object.
typedef struct scanner_interfaces__msg__Object__Sequence
{
  scanner_interfaces__msg__Object * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} scanner_interfaces__msg__Object__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SCANNER_INTERFACES__MSG__DETAIL__OBJECT__STRUCT_H_
