cimport cyquant.ctypes as c
cimport cyquant.dimensions as d
import cyquant.dimensions as d

from libc.math cimport fabs, fmax

cdef class SIUnit:
    cdef c.UData data

    cpdef is_of(SIUnit self, d.Dimensions dimensions)

    cpdef promote(SIUnit self, object value)
    cpdef demote(SIUnit self, Quantity value)


    cpdef bint compatible(SIUnit self, SIUnit other)
    cpdef approx(SIUnit self, SIUnit other, double rtol=*, double atol=*)
    cpdef cmp(SIUnit self, SIUnit other)


    cpdef SIUnit exp(SIUnit self, double power)

cdef class Quantity:
    cdef c.UData udata
    cdef double c_value
    cdef object py_value

    cdef double rescale(Quantity self, const c.UData& units) except -1.0

    cpdef is_of(Quantity self, d.Dimensions dimensions)

    cpdef get_as(Quantity self, SIUnit units)
    cpdef round_as(Quantity self, SIUnit units)

    cpdef Quantity cvt_to(Quantity self, SIUnit units)
    cpdef Quantity round_to(Quantity self, SIUnit units)

    #TODO: think abuot how best to handle approximation

    cpdef r_approx(Quantity self, Quantity other, double rtol=*)
    cpdef a_approx(Quantity self, Quantity other, double atol=*)
    cpdef q_approx(Quantity self, Quantity other, Quantity qtol)

    cpdef bint compatible(Quantity self, Quantity other)

    cpdef Quantity exp(Quantity self, double power)


cdef inline mul_units(SIUnit lhs, SIUnit rhs):
    cdef c.Error error_code
    cdef SIUnit ret = SIUnit.__new__(SIUnit)
    error_code = c.mul_udata(ret.data, lhs.data, rhs.data)
    if error_code == c.Success:
        return ret

    raise RuntimeError("Unknow Error Occurred: %i" % error_code)

cdef inline div_units(SIUnit lhs, SIUnit rhs):
    cdef c.Error error_code
    cdef SIUnit ret = SIUnit.__new__(SIUnit)
    error_code = c.div_udata(ret.data, lhs.data, rhs.data)
    if error_code == c.Success:
        return ret

    if error_code == c.ZeroDiv:
        raise ZeroDivisionError()

    raise RuntimeError("Unknown Error Occurred: %d" % error_code)

cdef inline void get_udata(c.UData& out, SIUnit units):
    (&out)[0] = units.data

# parsing functions




cdef inline int unsafe_native_cmp(Quantity lhs, Quantity rhs, double eps=0):
    cdef double lhs_norm = lhs.c_value * lhs.udata.scale
    cdef double rhs_norm = rhs.c_value * rhs.udata.scale

    if lhs_norm > rhs_norm + eps:
        return 1
    if lhs_norm < rhs_norm - eps:
        return -1
    return 0


cdef inline int parse_q(Quantity out, object py_obj):
    cdef type value_type = type(py_obj)

    if value_type is Quantity:
        return q_to_q(out, py_obj)

    if value_type is SIUnit:
        return u_to_q(out, py_obj)


    out.udata.scale = 1
    out.udata.dimensions.exponents[:] = [0,0,0,0,0,0,0]

    if value_type is float or value_type is int:
        out.py_value = None
        out.c_value = py_obj
    else:
        out.py_value = py_obj

    return c.Success

cdef inline int q_to_q(Quantity out, Quantity py_obj):
    out.py_value = py_obj.py_value
    out.c_value = py_obj.c_value
    out.udata = py_obj.udata
    return c.Success

cdef inline int u_to_q(Quantity out, SIUnit py_obj):
    out.py_value = None
    out.c_value = 1.0
    out.udata = py_obj.data
    return c.Success

cdef inline q_assign_mul(Quantity out, object py_obj):
    cdef type value_type = type(py_obj)
    if value_type is Quantity:
        return q_assign_mul_q(out, py_obj)
    if value_type is float or value_type is int:
        return q_assign_mul_d(out, py_obj)
    if value_type is SIUnit:
        return q_assign_mul_u(out, py_obj)
    return q_assign_mul_o(out, py_obj)


cdef inline q_assign_mul_q(Quantity out, Quantity rhs):
    c.mul_udata(out.udata, out.udata, rhs.udata)

    if out.py_value is None and rhs.py_value is None:
        out.c_value = out.c_value * rhs.c_value
        return c.Success

    if out.py_value is None:
        out.py_value = out.c_value

    if rhs.py_value is None:
        out.py_value = out.py_value * rhs.c_value
    else:
        out.py_value = out.py_value * rhs.py_value

    return q_norm(out)

cdef inline q_assign_mul_u(Quantity out, SIUnit rhs):
    return c.mul_udata(out.udata, out.udata, rhs.data)

cdef inline q_assign_mul_d(Quantity out, double rhs):
    if out.py_value is None:
        out.c_value = out.c_value * rhs
    else:
        out.py_value = out.py_value * rhs
    return c.Success

cdef inline q_assign_mul_o(Quantity out, object rhs):
    if out.py_value is None:
        out.py_value = out.c_value * rhs
    else:
        out.py_value = out.py_value * rhs
    return c.Success

cdef inline q_assign_div(Quantity out, object rhs):
    cdef type value_type = type(rhs)
    if value_type is Quantity:
        return q_assign_div_q(out, rhs)
    if value_type is float or value_type is int:
        return q_assign_div_d(out, rhs)
    if value_type is SIUnit:
        return q_assign_div_u(out, rhs)
    return q_assign_div_o(out, rhs)

cdef inline q_assign_div_q(Quantity out, Quantity rhs):
    c.div_udata(out.udata, out.udata, rhs.udata)

    if out.py_value is None and rhs.py_value is None:
        if rhs.c_value == 0:
            return c.ZeroDiv
        out.c_value = out.c_value / rhs.c_value
        return c.Success

    if out.py_value is None:
        out.py_value = out.c_value

    if rhs.py_value is None:
        if rhs.c_value == 0:
            return c.ZeroDiv
        out.py_value = out.py_value / rhs.c_value
    else:
        out.py_value = out.py_value / rhs.py_value

    return q_norm(out)

cdef inline q_assign_div_u(Quantity out, SIUnit rhs):
    c.div_udata(out.udata, out.udata, rhs.data)

cdef inline q_assign_div_d(Quantity out, double rhs):
    if rhs == 0:
        return c.ZeroDiv

    if out.py_value is None:
        out.c_value = out.c_value / rhs
        return c.Success
    else:
        out.py_value = out.py_value / rhs
        return q_norm(out)


cdef inline q_assign_div_o(Quantity out, object rhs):
    if out.py_value is None:
        out.py_value = out.c_value / rhs
    else:
        out.py_value = out.py_value / rhs
    return q_norm(out)


cdef inline q_norm(Quantity out):
    cdef type ret_type = type(out.py_value)
    if ret_type is float or ret_type is int:
        out.c_value = out.py_value
        out.py_value = None

    return c.Success

cdef inline c_r_approx(double l, c.UData ul, double r, c.UData ur, double rtol):
    cdef int error_code
    cdef c.UData u_min
    cdef double epsilon

    error_code = c.min_udata(u_min, ul, ur)
    if error_code == c.Success:
        l = (l * ul.scale / u_min.scale)
        r = (r * ur.scale / u_min.scale)

        epsilon = fmax(1.0, fmax(fabs(l), fabs(r))) * rtol
        return fabs(l - r) <= fabs(epsilon)

    if error_code == c.DimensionMismatch:
        raise ValueError("Incompatible Units")

    raise RuntimeError("Unknown Error: %i" % error_code)

cdef inline py_r_approx(object lhs, c.UData u_lhs, object rhs, c.UData u_rhs, double rtol):
    cdef int error_code
    cdef c.UData u_min
    cdef object lhs_norm, rhs_norm, epsilon

    error_code = c.min_udata(u_min, u_lhs, u_rhs)
    if error_code == c.Success:
        lhs_norm = lhs * (u_lhs.scale / u_min.scale)
        rhs_norm = rhs * (u_rhs.scale / u_min.scale)

        epsilon = max(1.0, abs(lhs_norm), abs(rhs_norm)) * fabs(rtol)
        return abs(lhs_norm - rhs_norm) <= epsilon

    if error_code == c.DimensionMismatch:
        raise ValueError("Incompatible Units")

    raise RuntimeError("Unknown Error: %i" % error_code)

cdef inline c_a_approx(double l, c.UData ul, double r, c.UData ur, double epsilon):
    cdef c.UData u_min
    cdef l_norm, r_norm

    cdef error_code = c.min_udata(u_min, ul, ur)
    if error_code == c.Success:
        l_norm = l * (ul.scale / u_min.scale)
        r_norm = r * (ur.scale / u_min.scale)

        return fabs(l_norm - r_norm) <= fabs(epsilon)

    if error_code == c.DimensionMismatch:
        raise ValueError("incompatible units")

    raise RuntimeError("unknown error ({})".format(error_code))

cdef inline py_a_approx(object l, c.UData ul, object r, c.UData ur, double epsilon):
    cdef c.UData u_min
    cdef object l_norm, r_norm

    cdef error_code = c.min_udata(u_min, ul, ur)
    if error_code == c.Success:
        l_norm = l * (ul.scale / u_min.scale)
        r_norm = r * (ur.scale / u_min.scale)

        return abs(l_norm - r_norm) <= fabs(epsilon)

    if error_code == c.DimensionMismatch:
        raise ValueError("incompatible units")

    raise RuntimeError("unknown error ({})".format(error_code))

cdef inline c_q_approx(double l, c.UData ul, double r, c.UData ur, double q, c.UData uq):
    if not c.eq_ddata(ul.dimensions, uq.dimensions):
        raise ValueError("incompatible units")
    if not c.eq_ddata(ur.dimensions, uq.dimensions):
        raise ValueError("incompatible units")

    l = l * ul.scale / uq.scale
    r = r * ur.scale / uq.scale

    return fabs(l - r) <= fabs(q)

cdef inline py_q_approx(object l, c.UData ul, object r, c.UData ur, object q, c.UData uq):
    if not c.eq_ddata(ul.dimensions, uq.dimensions):
        raise ValueError("incompatible units")
    if not c.eq_ddata(ur.dimensions, uq.dimensions):
        raise ValueError("incompatible units")

    cdef object l_norm, r_norm

    l_norm = l * (ul.scale / uq.scale)
    r_norm = r * (ur.scale / uq.scale)

    return abs(l_norm - r_norm) <= abs(q)


