// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from scanner_interfaces:msg/CameraLocations.idl
// generated code does not contain a copyright notice
#include "scanner_interfaces/msg/detail/camera_locations__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `locations`
#include "scanner_interfaces/msg/detail/location__functions.h"

bool
scanner_interfaces__msg__CameraLocations__init(scanner_interfaces__msg__CameraLocations * msg)
{
  if (!msg) {
    return false;
  }
  // locations
  if (!scanner_interfaces__msg__Location__Sequence__init(&msg->locations, 0)) {
    scanner_interfaces__msg__CameraLocations__fini(msg);
    return false;
  }
  return true;
}

void
scanner_interfaces__msg__CameraLocations__fini(scanner_interfaces__msg__CameraLocations * msg)
{
  if (!msg) {
    return;
  }
  // locations
  scanner_interfaces__msg__Location__Sequence__fini(&msg->locations);
}

bool
scanner_interfaces__msg__CameraLocations__are_equal(const scanner_interfaces__msg__CameraLocations * lhs, const scanner_interfaces__msg__CameraLocations * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // locations
  if (!scanner_interfaces__msg__Location__Sequence__are_equal(
      &(lhs->locations), &(rhs->locations)))
  {
    return false;
  }
  return true;
}

bool
scanner_interfaces__msg__CameraLocations__copy(
  const scanner_interfaces__msg__CameraLocations * input,
  scanner_interfaces__msg__CameraLocations * output)
{
  if (!input || !output) {
    return false;
  }
  // locations
  if (!scanner_interfaces__msg__Location__Sequence__copy(
      &(input->locations), &(output->locations)))
  {
    return false;
  }
  return true;
}

scanner_interfaces__msg__CameraLocations *
scanner_interfaces__msg__CameraLocations__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  scanner_interfaces__msg__CameraLocations * msg = (scanner_interfaces__msg__CameraLocations *)allocator.allocate(sizeof(scanner_interfaces__msg__CameraLocations), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(scanner_interfaces__msg__CameraLocations));
  bool success = scanner_interfaces__msg__CameraLocations__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
scanner_interfaces__msg__CameraLocations__destroy(scanner_interfaces__msg__CameraLocations * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    scanner_interfaces__msg__CameraLocations__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
scanner_interfaces__msg__CameraLocations__Sequence__init(scanner_interfaces__msg__CameraLocations__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  scanner_interfaces__msg__CameraLocations * data = NULL;

  if (size) {
    data = (scanner_interfaces__msg__CameraLocations *)allocator.zero_allocate(size, sizeof(scanner_interfaces__msg__CameraLocations), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = scanner_interfaces__msg__CameraLocations__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        scanner_interfaces__msg__CameraLocations__fini(&data[i - 1]);
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
scanner_interfaces__msg__CameraLocations__Sequence__fini(scanner_interfaces__msg__CameraLocations__Sequence * array)
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
      scanner_interfaces__msg__CameraLocations__fini(&array->data[i]);
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

scanner_interfaces__msg__CameraLocations__Sequence *
scanner_interfaces__msg__CameraLocations__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  scanner_interfaces__msg__CameraLocations__Sequence * array = (scanner_interfaces__msg__CameraLocations__Sequence *)allocator.allocate(sizeof(scanner_interfaces__msg__CameraLocations__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = scanner_interfaces__msg__CameraLocations__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
scanner_interfaces__msg__CameraLocations__Sequence__destroy(scanner_interfaces__msg__CameraLocations__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    scanner_interfaces__msg__CameraLocations__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
scanner_interfaces__msg__CameraLocations__Sequence__are_equal(const scanner_interfaces__msg__CameraLocations__Sequence * lhs, const scanner_interfaces__msg__CameraLocations__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!scanner_interfaces__msg__CameraLocations__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
scanner_interfaces__msg__CameraLocations__Sequence__copy(
  const scanner_interfaces__msg__CameraLocations__Sequence * input,
  scanner_interfaces__msg__CameraLocations__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(scanner_interfaces__msg__CameraLocations);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    scanner_interfaces__msg__CameraLocations * data =
      (scanner_interfaces__msg__CameraLocations *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!scanner_interfaces__msg__CameraLocations__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          scanner_interfaces__msg__CameraLocations__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!scanner_interfaces__msg__CameraLocations__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
