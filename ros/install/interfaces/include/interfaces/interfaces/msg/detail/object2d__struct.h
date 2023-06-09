// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Object2d.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__OBJECT2D__STRUCT_H_
#define INTERFACES__MSG__DETAIL__OBJECT2D__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Object2d in the package interfaces.
/**
  * characteristics of a tracked object
 */
typedef struct interfaces__msg__Object2d
{
  int8_t id;
  double x;
  double y;
  int64_t x_max;
  int64_t y_max;
  double radius;
  int64_t diff;
} interfaces__msg__Object2d;

// Struct for a sequence of interfaces__msg__Object2d.
typedef struct interfaces__msg__Object2d__Sequence
{
  interfaces__msg__Object2d * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Object2d__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__OBJECT2D__STRUCT_H_
