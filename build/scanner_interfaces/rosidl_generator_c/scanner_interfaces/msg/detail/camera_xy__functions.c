// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from scanner_interfaces:msg/CameraXY.idl
// generated code does not contain a copyright notice
#include "scanner_interfaces/msg/detail/camera_xy__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
scanner_interfaces__msg__CameraXY__init(scanner_interfaces__msg__CameraXY * msg)
{
  if (!msg) {
    return false;
  }
  // x
  // y
  // x_max
  // y_max
  // found
  // fps
  return true;
}

void
scanner_interfaces__msg__CameraXY__fini(scanner_interfaces__msg__CameraXY * msg)
{
  if (!msg) {
    return;
  }
  // x
  // y
  // x_max
  // y_max
  // found
  // fps
}

bool
scanner_interfaces__msg__CameraXY__are_equal(const scanner_interfaces__msg__CameraXY * lhs, const scanner_interfaces__msg__CameraXY * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // x_max
  if (lhs->x_max != rhs->x_max) {
    return false;
  }
  // y_max
  if (lhs->y_max != rhs->y_max) {
    return false;
  }
  // found
  if (lhs->found != rhs->found) {
    return false;
  }
  // fps
  if (lhs->fps != rhs->fps) {
    return false;
  }
  return true;
}

bool
scanner_interfaces__msg__CameraXY__copy(
  const scanner_interfaces__msg__CameraXY * input,
  scanner_interfaces__msg__CameraXY * output)
{
  if (!input || !output) {
    return false;
  }
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // x_max
  output->x_max = input->x_max;
  // y_max
  output->y_max = input->y_max;
  // found
  output->found = input->found;
  // fps
  output->fps = input->fps;
  return true;
}

scanner_interfaces__msg__CameraXY *
scanner_interfaces__msg__CameraXY__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  scanner_interfaces__msg__CameraXY * msg = (scanner_interfaces__msg__CameraXY *)allocator.allocate(sizeof(scanner_interfaces__msg__CameraXY), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(scanner_interfaces__msg__CameraXY));
  bool success = scanner_interfaces__msg__CameraXY__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
scanner_interfaces__msg__CameraXY__destroy(scanner_interfaces__msg__CameraXY * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    scanner_interfaces__msg__CameraXY__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
scanner_interfaces__msg__CameraXY__Sequence__init(scanner_interfaces__msg__CameraXY__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  scanner_interfaces__msg__CameraXY * data = NULL;

  if (size) {
    data = (scanner_interfaces__msg__CameraXY *)allocator.zero_allocate(size, sizeof(scanner_interfaces__msg__CameraXY), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = scanner_interfaces__msg__CameraXY__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        scanner_interfaces__msg__CameraXY__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
scanner_interfaces__msg__CameraXY__Sequence__fini(scanner_interfaces__msg__CameraXY__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      scanner_interfaces__msg__CameraXY__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

scanner_interfaces__msg__CameraXY__Sequence *
scanner_interfaces__msg__CameraXY__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  scanner_interfaces__msg__CameraXY__Sequence * array = (scanner_interfaces__msg__CameraXY__Sequence *)allocator.allocate(sizeof(scanner_interfaces__msg__CameraXY__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = scanner_interfaces__msg__CameraXY__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
scanner_interfaces__msg__CameraXY__Sequence__destroy(scanner_interfaces__msg__CameraXY__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    scanner_interfaces__msg__CameraXY__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
scanner_interfaces__msg__CameraXY__Sequence__are_equal(const scanner_interfaces__msg__CameraXY__Sequence * lhs, const scanner_interfaces__msg__CameraXY__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!scanner_interfaces__msg__CameraXY__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
scanner_interfaces__msg__CameraXY__Sequence__copy(
  const scanner_interfaces__msg__CameraXY__Sequence * input,
  scanner_interfaces__msg__CameraXY__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(scanner_interfaces__msg__CameraXY);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    scanner_interfaces__msg__CameraXY * data =
      (scanner_interfaces__msg__CameraXY *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!scanner_interfaces__msg__CameraXY__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          scanner_interfaces__msg__CameraXY__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!scanner_interfaces__msg__CameraXY__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
