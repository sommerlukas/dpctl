#                      Data Parallel Control (dpctl)
#
# Copyright 2020-2025 Intel Corporation
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
# cython: linetrace=True

from .._backend cimport (DPCTLRawKernelArg_Create, DPCTLRawKernelArg_Delete)

cdef class _RawKernelArg:
    def __dealloc__(self):
        if(self._arg_ref):
            DPCTLRawKernelArg_Delete(self._arg_ref)

ctypedef unsigned long long void_ptr

cdef class RawKernelArg:
    """
    RawKernelArg(count, data)
    Python class representing the ``raw_kernel_arg`` class from the Raw Kernel
    Argument oneAPI SYCL extension representing a kernel argument as raw bytes.

    Args:
        count (int)
            Size of the argument in bytes.
            Expected to be positive.
        
        data (unsigned long int/void*)
            Pointer specifying the address of the raw kernel argument bytes.
    """
    def __cinit__(self, Py_ssize_t count, void_ptr data):
        cdef void* ptr = <void*>data
        self._arg_ref = DPCTLRawKernelArg_Create(count, ptr)

    property _ref:
        """Returns the address of the C API ``DPCTLSyclRawKernelArgRef``
        pointer as a ``size_t``.
        """
        
        def __get__(self):
            return <size_t>self._arg_ref
