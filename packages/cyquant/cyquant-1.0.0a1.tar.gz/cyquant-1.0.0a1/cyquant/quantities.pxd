cimport cyquant.ctypes as c
cimport cyquant.dimensions as d
import cyquant.dimensions as d

cdef class SIUnit:
    cdef c.UData data

    cpdef is_of(SIUnit self, d.Dimensions dimensions)

    cpdef promote(SIUnit self, double value)
    cpdef demote(SIUnit self, Quantity value)


    cpdef bint compatible(SIUnit self, SIUnit other)
    cpdef approx(SIUnit self, SIUnit other, double rtol=*, double atol=*)
    cpdef cmp(SIUnit self, SIUnit other)


    cpdef SIUnit exp(SIUnit self, double power)

cdef class Quantity:
    cdef c.QData data

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

    cpdef cmp(Quantity self, Quantity other)

    cpdef Quantity exp(Quantity self, double power)

cdef inline Quantity mul_quantities(const c.QData& lhs, const c.QData& rhs):
    cdef c.Error error_code
    cdef Quantity ret = Quantity.__new__(Quantity)
    error_code = c.mul_qdata(ret.data, lhs, rhs)
    if error_code == c.Success:
        return ret

    raise RuntimeError("Unknown Error Occurred: %i" % error_code)

cdef inline SIUnit mul_units(const c.UData& lhs, const c.UData& rhs):
    cdef c.Error error_code
    cdef SIUnit ret = SIUnit.__new__(SIUnit)
    error_code = c.mul_udata(ret.data, lhs, rhs)
    if error_code == c.Success:
        return ret

    raise RuntimeError("Unknow Error Occurred: %i" % error_code)

cdef inline Quantity div_quantities(const c.QData& lhs, const c.QData& rhs):
    cdef c.Error error_code
    cdef Quantity ret = Quantity.__new__(Quantity)
    error_code = c.div_qdata(ret.data, lhs, rhs)
    if error_code == c.Success:
        return ret

    if error_code == c.ZeroDiv:
        raise ZeroDivisionError()

    raise RuntimeError("Unknown Error Occurred: %d" % error_code)

cdef inline SIUnit div_units(const c.UData& lhs, const c.UData& rhs):
    cdef c.Error error_code
    cdef SIUnit ret = SIUnit.__new__(SIUnit)
    error_code = c.div_udata(ret.data, lhs, rhs)
    if error_code == c.Success:
        return ret

    if error_code == c.ZeroDiv:
        raise ZeroDivisionError()

    raise RuntimeError("Unknown Error Occurred: %d" % error_code)

# parsing functions

cdef inline c.Operand parse_uoperand(c.QData& out, object py_obj):
    op_type = type(py_obj)
    if op_type is float or op_type is int:
        out.quantity = <double>py_obj
        out.units.scale = 1.0
        out.units.dimensions.exponents[:] = [0,0,0,0,0,0,0]
        return c.QUANTITY
    elif op_type is SIUnit:
        out.quantity = 1.0
        return extract_udata(out.units, py_obj)
    elif op_type is Quantity:
        return extract_qdata(out, py_obj)
    else:
        return c.OBJECT


cdef inline c.Operand parse_qoperand(c.QData& out, object py_obj):
    op_type = type(py_obj)
    if op_type is Quantity:
        return extract_qdata(out, py_obj)
    elif op_type is float or op_type is int:
        out.quantity = <double>py_obj
        out.units.scale = 1.0
        out.units.dimensions.exponents[:] = [0,0,0,0,0,0,0]
        return c.QUANTITY
    return c.OBJECT


cdef inline c.Operand extract_udata(c.UData& out, SIUnit py_obj):
    (&out)[0] = py_obj.data
    return c.UNIT


cdef inline c.Operand extract_qdata(c.QData& out, Quantity py_obj):
    (&out)[0] = py_obj.data
    return c.QUANTITY
