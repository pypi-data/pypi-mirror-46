cimport cyquant.ctypes as c

cdef class Dimensions:
    cdef c.DData data

    cpdef bint approx(Dimensions self, Dimensions other)

    cpdef Dimensions exp(Dimensions self, double power)