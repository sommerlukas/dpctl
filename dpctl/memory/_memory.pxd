#                      Data Parallel Control (dpctl)
#
# Copyright 2020-2021 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# distutils: language = c++
# cython: language_level=3

""" This file has the Cython function declarations for the functions defined
in dpctl.memory._memory.pyx.

"""

from .._backend cimport DPCTLSyclUSMRef
from .._sycl_context cimport SyclContext
from .._sycl_device cimport SyclDevice
from .._sycl_queue cimport SyclQueue


cdef public class _Memory [object Py_MemoryObject, type Py_MemoryType]:
    cdef DPCTLSyclUSMRef memory_ptr
    cdef Py_ssize_t nbytes
    cdef SyclQueue queue
    cdef object refobj

    cdef _cinit_empty(self)
    cdef _cinit_alloc(self, Py_ssize_t alignment, Py_ssize_t nbytes,
                      bytes ptr_type, SyclQueue queue)
    cdef _cinit_other(self, object other)
    cdef _getbuffer(self, Py_buffer *buffer, int flags)

    cpdef copy_to_host(self, object obj=*)
    cpdef copy_from_host(self, object obj)
    cpdef copy_from_device(self, object obj)

    cpdef bytes tobytes(self)

    @staticmethod
    cdef public SyclDevice get_pointer_device(DPCTLSyclUSMRef p, SyclContext ctx)
    @staticmethod
    cdef public bytes get_pointer_type(DPCTLSyclUSMRef p, SyclContext ctx)


cdef public class MemoryUSMShared(_Memory) [object PyMemoryUSMSharedObject, type PyMemoryUSMSharedType]:
    pass


cdef public class MemoryUSMHost(_Memory) [object PyMemoryUSMHostObject, type PyMemoryUSMHostType]:
    pass


cdef public class MemoryUSMDevice(_Memory) [object PyMemoryUSMDeviceObject, type PyMemoryUSMDeviceType]:
    pass
