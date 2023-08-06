from libc.string cimport memcmp
from libc.math cimport fabs, fmax

cdef struct DData:
    float exponents[7]

cdef struct UData:
    double scale
    DData dimensions

cdef inline bint fapprox(double a, double b, double rtol, double atol):
    cdef double epsilon = fabs(fmax(atol, rtol * fmax(1, fmax(a, b))))
    return fabs(a - b) <= epsilon

cdef inline bint eq_ddata(const DData& lhs, const DData& rhs, float atol=1e-9):
    cdef size_t i
    for i in range(7):
        if fabs(lhs.exponents[i] - rhs.exponents[i]) > atol:
            return False
    return True

cdef inline bint eq_udata(const UData& lhs, const UData& rhs, double atol=1e-9):
    if fabs(lhs.scale - rhs.scale) > atol:
        return False
    return eq_ddata(lhs.dimensions, rhs.dimensions, atol)


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
    cdef size_t i
    for i in range(7):
        out.exponents[i] = lhs.exponents[i] + rhs.exponents[i]
    return Success

#Success
cdef inline Error div_ddata(DData& out, const DData& lhs, const DData& rhs):
    cdef size_t i
    for i in range(7):
        out.exponents[i] = lhs.exponents[i] - rhs.exponents[i]
    return Success

#Success
cdef inline Error pow_ddata(DData& out, const DData& lhs, double power):
    cdef size_t i
    for i in range(7):
        out.exponents[i] = lhs.exponents[i] * power
    return Success

cdef inline Error inv_ddata(DData& out, const DData& src):
    cdef size_t i
    for i in range(7):
        out.exponents[i] = -src.exponents[i]
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

cdef inline Error inv_udata(UData& out, const UData& src):
    # if src.scale == 0:
    #     return c.ZeroDiv
    out.scale = 1.0 / src.scale
    return inv_ddata(out.dimensions, src.dimensions)


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
