from .._backend cimport (DPCTLRawKernelArg_Create, DPCTLRawKernelArg_Delete)

cdef class _RawKernelArg:
    def __dealloc__(self):
        if(self._arg_ref):
            DPCTLRawKernelArg_Delete(self._arg_ref)

ctypedef unsigned long long void_ptr

cdef class RawKernelArg:
    """
    TODO: Add documentation.
    """
    def __cinit__(self, Py_ssize_t count, void_ptr data):
        cdef void* ptr = <void*>data
        self._arg_ref = DPCTLRawKernelArg_Create(count, ptr)

    cdef DPCTLSyclRawKernelArgRef get_arg_ref(self):
        return self._arg_ref

    property _ref:
        def __get__(self):
            return <size_t>self._arg_ref
