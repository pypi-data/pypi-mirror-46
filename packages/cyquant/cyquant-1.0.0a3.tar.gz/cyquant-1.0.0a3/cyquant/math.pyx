cimport cyquant.ctypes as c

cimport cyquant.quantities as q
import cyquant.quantities as q

from libc cimport math

from cyquant import si

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

    error_code = c.min_udata(norm_udata, y.data.units, x.data.units)

    if error_code == c.Success:
        x_norm = c.unsafe_extract_quantity(x.data, norm_udata)
        y_norm = c.unsafe_extract_quantity(y.data, norm_udata)

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

    error_code = c.min_udata(ret.data.units, y.data.units, x.data.units)

    if error_code == c.Success:
        x_norm = c.unsafe_extract_quantity(x.data, ret.data.units)
        y_norm = c.unsafe_extract_quantity(y.data, ret.data.units)

        ret.data.quantity = math.hypot(x_norm, y_norm)
        return ret

    if error_code == c.DimensionMismatch:
        raise ValueError("unit mismatch")

    raise RuntimeError("Unknown Error Occurred: %i" % error_code)

#todo: exp/log/etc