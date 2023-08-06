cimport cyquant.ctypes as c

cimport cyquant.quantities as q
import cyquant.quantities as q

from libc cimport math

from cyquant import si

pi = math.pi * si.radians
eta = pi / 2
tau = pi * 2

cpdef sin(q.Quantity value):
    cdef double rads = value.get_as(si.radians)
    cdef double ratio = math.sin(rads)
    return si.unity.promote(ratio)

cpdef cos(q.Quantity value):
    cdef double rads = value.get_as(si.radians)
    cdef double ratio = math.cos(rads)
    return si.unity.promote(ratio)

cpdef tan(q.Quantity value):
    cdef double rads = value.get_as(si.radians)
    cdef double ratio = math.tan(rads)
    return si.unity.promote(ratio)

cpdef acos(q.Quantity value):
    cdef double ratio = value.get_as(si.unity)
    if ratio < -1 or ratio > 1:
        raise ValueError("math domain error")
    cdef double rads = math.acos(ratio)
    return si.radians.promote(rads)

cpdef asin(q.Quantity value):
    cdef double ratio = value.get_as(si.unity)
    if ratio < -1 or ratio > 1:
        raise ValueError("math domain error")
    cdef double rads = math.asin(ratio)
    return si.radians.promote(rads)

cpdef atan(q.Quantity value):
    cdef double ratio = value.get_as(si.unity)
    cdef double rads = math.atan(ratio)
    return si.radians.promote(rads)

cpdef atan2(q.Quantity y, q.Quantity x):
    cdef int error_code
    cdef c.UData norm_udata
    cdef double x_norm, y_norm, rads

    error_code = c.min_udata(norm_udata, y.udata, x.udata)

    if error_code == c.Success:
        x_norm = x.rescale(norm_udata) * (x.c_value if x.py_value is None else float(x.py_value))
        y_norm = y.rescale(norm_udata) * (y.c_value if y.py_value is None else float(y.py_value))

        if x_norm == 0 and y_norm == 0:
            raise ValueError("math domain error")

        rads = math.atan2(y_norm, x_norm)
        return si.radians.promote(rads)

    if error_code == c.DimensionMismatch:
        raise ValueError("unit mismatch")

    raise RuntimeError("Unknown Error Occurred: %i" % error_code)



cpdef hypot(q.Quantity x, q.Quantity y):
    cdef q.Quantity ret = q.Quantity.__new__(q.Quantity)
    cdef int error_code
    cdef double x_norm, y_norm

    error_code = c.min_udata(ret.udata, y.udata, x.udata)

    if error_code == c.Success:
        x_norm = x.rescale(ret.udata) * (x.c_value if x.py_value is None else float(x.py_value))
        y_norm = y.rescale(ret.udata) * (y.c_value if y.py_value is None else float(y.py_value))

        ret.py_value = None
        ret.c_value = math.hypot(x_norm, y_norm)
        return ret

    if error_code == c.DimensionMismatch:
        raise ValueError("unit mismatch")

    raise RuntimeError("Unknown Error Occurred: %i" % error_code)

#todo: exp/log/etc