from libc.string cimport memcmp
from libc.math cimport fabs, fmax

cdef struct DData:
    double exponents[7]

cdef struct UData:
    double scale
    DData dimensions

cdef struct QData:
    double quantity
    UData units

cdef enum Operand:
    OBJECT = 1
    UNIT = 2
    QUANTITY = 4

cdef inline bint fapprox(double a, double b, double rtol, double atol):
    cdef double epsilon = fabs(fmax(atol, rtol * fmax(1, fmax(a, b))))
    return fabs(a - b) <= epsilon

cdef inline bint eq_ddata(const DData& lhs, const DData& rhs):
    return memcmp(&lhs, &rhs, sizeof(DData)) == 0

cdef inline double unsafe_extract_quantity(const QData& src, const UData& units):
    return src.quantity * src.units.scale / units.scale


# begin error code convention interface

cdef enum Error:
    Success = 0
    DimensionMismatch = 1
    ZeroDiv = 2
    #Overflow = 4
    Unknown = 0x80000000

# begin ddata functions

#Success
cdef inline Error mul_ddata(DData& out, const DData& lhs, const DData& rhs):
    cdef int i
    for i in range(7):
        out.exponents[i] = lhs.exponents[i] + rhs.exponents[i]
    return Success

#Success
cdef inline Error div_ddata(DData& out, const DData& lhs, const DData& rhs):
    cdef int i
    for i in range(7):
        out.exponents[i] = lhs.exponents[i] - rhs.exponents[i]
    return Success

#Success
cdef inline Error pow_ddata(DData& out, const DData& lhs, double power):
    cdef int i
    for i in range(7):
        out.exponents[i] = lhs.exponents[i] * power
    return Success

# begin udata functions

#Success
cdef inline Error mul_udata(UData& out, const UData& lhs, const UData& rhs):
    #todo: overflow checks
    out.scale = lhs.scale * rhs.scale
    return mul_ddata(out.dimensions, lhs.dimensions, rhs.dimensions)

#Success
#ZeroDiv
cdef inline Error div_udata(UData& out, const UData& lhs, const UData& rhs):
    if rhs.scale == 0:
        return ZeroDiv
    out.scale = lhs.scale / rhs.scale
    return div_ddata(out.dimensions, lhs.dimensions, rhs.dimensions)

#Success
cdef inline Error pow_udata(UData& out, const UData& lhs, double power):
    #todo: overflow checks
    out.scale = lhs.scale ** power
    return pow_ddata(out.dimensions, lhs.dimensions, power)

#Success
#DimensionMismatch
cdef inline Error cmp_udata(int& out, const UData& lhs, const UData& rhs):
    if not eq_ddata(lhs.dimensions, rhs.dimensions):
        return DimensionMismatch

    if lhs.scale > rhs.scale:
        (&out)[0] = 1
    elif lhs.scale < rhs.scale:
        (&out)[0] = -1
    else:
        (&out)[0] = 0

    return Success

#Success
#DimensionMismatch
cdef inline Error min_udata(UData& out, const UData& lhs, const UData& rhs):
    if not eq_ddata(lhs.dimensions, rhs.dimensions):
        return DimensionMismatch

    if lhs.scale < rhs.scale:
        (&out)[0] = lhs
    else:
        (&out)[0] = rhs

    return Success

## begin qdata functions

#Success
cdef inline Error mul_qdata(QData& out, const QData& lhs, const QData& rhs):
    cdef Error error_code

    error_code = mul_udata(out.units, lhs.units, rhs.units)
    if error_code:
        return error_code

    out.quantity = lhs.quantity * rhs.quantity

    return Success

#Success
#ZeroDiv
cdef inline Error div_qdata(QData& out, const QData& lhs, const QData& rhs):
    if rhs.quantity == 0.0:
        return ZeroDiv

    cdef Error error_code

    error_code = div_udata(out.units, lhs.units, rhs.units)
    if error_code:
        return error_code

    out.quantity = lhs.quantity / rhs.quantity
    return Success

#Success
cdef inline Error pow_qdata(QData& out, const QData& lhs, double rhs):
    cdef Error error_code

    error_code = pow_udata(out.units, lhs.units, rhs)
    if error_code:
        return error_code

    out.quantity = lhs.quantity ** rhs

    return Success

#Success
#DimensionMismatch
cdef inline Error add_qdata(QData& out, const QData& lhs, const QData& rhs):
    cdef Error error_code

    error_code = min_udata(out.units, lhs.units, rhs.units)
    if error_code:
        return error_code

    out.quantity = unsafe_extract_quantity(lhs, out.units)
    out.quantity += unsafe_extract_quantity(rhs, out.units)

    return Success

#Success
#DimensionMismatch
cdef inline Error sub_qdata(QData& out, const QData& lhs, const QData& rhs):
    cdef Error error_code

    error_code = min_udata(out.units, lhs.units, rhs.units)
    if error_code:
        return error_code

    out.quantity = unsafe_extract_quantity(lhs, out.units)
    out.quantity -= unsafe_extract_quantity(rhs, out.units)
    return Success

#Success
#DimensionMismatch
cdef inline Error cvt_quantity(QData& out, const QData& src, const UData& units):
    cdef Error error_code

    error_code = extract_quantity(out.quantity, src, units)
    if error_code:
        return error_code

    out.units = units
    return Success

#Success
#DimensionMismatch
cdef inline Error extract_quantity(double& out, const QData& src, const UData& units):
    if not eq_ddata(src.units.dimensions, units.dimensions):
        return DimensionMismatch
    (&out)[0] = unsafe_extract_quantity(src, units)
    return Success

#Success
#DimensionMismatch
cdef inline Error cmp_qdata(int& out, const QData& lhs, const QData& rhs):
    if not eq_ddata(lhs.units.dimensions, rhs.units.dimensions):
        return DimensionMismatch

    cdef lhs_norm = lhs.quantity * lhs.units.scale
    cdef rhs_norm = rhs.quantity * rhs.units.scale

    if lhs_norm > rhs_norm:
        (&out)[0] = 1
    elif lhs_norm < rhs_norm:
        (&out)[0] = -1
    else:
        (&out)[0] = 0

    return Success

