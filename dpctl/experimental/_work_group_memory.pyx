cdef class WorkGroupMemory:
    """
    TODO: Add documentation.
    """
    def __cinit__(self, Py_ssize_t nbytes):
        self.nbytes = nbytes

    property nbytes:
        """Extent of this USM buffer in bytes."""
        def __get__(self):
            return self.nbytes


