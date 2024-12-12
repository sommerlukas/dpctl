from .._backend cimport DPCTLSyclRawKernelArgRef

import ctypes

cdef public api class _RawKernelArg [
    object Py_RawKernelArgObject, type Py_RawKernelArgType
]:
    cdef DPCTLSyclRawKernelArgRef _arg_ref

cdef public api class RawKernelArg(_RawKernelArg) [
    object PyRawKernelArgObject, type PyRawKernelArgType
]:

    cdef DPCTLSyclRawKernelArgRef get_arg_ref(self)
