#!python
#cython: language_level=3

cimport cyquant.ctypes as c
cimport cyquant.dimensions as d
import cyquant.dimensions as d

from libc.math cimport round, fabs, fmax

cdef double UNIT_SCALE_RTOL = 1e-12

cdef class SIUnit:


    @staticmethod
    def SetEqRelTol(double rtol):
        global UNIT_SCALE_RTOL
        if rtol < 0:
            raise ValueError("Relative tolerance must be greater than 0.")
        UNIT_SCALE_RTOL = rtol

    @staticmethod
    def GetEqRelTol():
        return UNIT_SCALE_RTOL

    @staticmethod
    def Unit(scale=1, kg=0, m=0, s=0, k=0, a=0, mol=0, cd=0):
        return SIUnit(scale, d.Dimensions(kg, m, s, k, a, mol, cd))

    @property
    def scale(self):
        return self.data.scale

    @property
    def dimensions(self):
        cdef d.Dimensions dims = d.Dimensions.__new__(d.Dimensions)
        dims.data = self.data.dimensions
        return dims

    @property
    def kg(self):
        return self.data.dimensions.exponents[0]

    @property
    def m(self):
        return self.data.dimensions.exponents[1]

    @property
    def s(self):
        return self.data.dimensions.exponents[2]

    @property
    def k(self):
        return self.data.dimensions.exponents[3]

    @property
    def a(self):
        return self.data.dimensions.exponents[4]

    @property
    def mol(self):
        return self.data.dimensions.exponents[5]

    @property
    def cd(self):
        return self.data.dimensions.exponents[6]

    def __init__(SIUnit self, double scale=1.0, d.Dimensions dims=d.dimensionless_t):
        if scale <= 0:
            raise ValueError("arg 'scale' must be greater than 0")
        if type(dims) is not d.Dimensions:
            raise TypeError("Expected Dimensions")
        self.data.scale = scale
        self.data.dimensions = dims.data

    """
    Wrapping Methods
    """

    def pack(SIUnit self, *args):
        return self.quantities(args)

    def unpack(SIUnit self, *args):
        return self.values(args)

    def quantities(SIUnit self, iterable):
        for value in iterable:
            yield self.promote(value)

    def values(SIUnit self, iterable):
        for quantity in iterable:
            yield self.demote(quantity)

    cpdef promote(SIUnit self, double value):
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = value
        ret.data.units = self.data
        return ret

    cpdef demote(SIUnit self, Quantity value):
        cdef int error_code
        cdef double ret
        error_code = c.extract_quantity(ret, value.data, self.data)
        if error_code == c.Success:
            return ret

        if error_code == c.DimensionMismatch:
            raise ValueError("unit mismatch")


        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __call__(SIUnit self, iterable):
        return self.quantities(iterable)

    """
    Comparison Methods
    """

    cpdef is_of(SIUnit self, d.Dimensions dims):
        if dims is None:
            raise TypeError()
        return c.eq_ddata(self.data.dimensions, dims.data)

    def __eq__(lhs, rhs):
        if not type(lhs) is SIUnit:
            return NotImplemented
        if not type(rhs) is SIUnit:
            return NotImplemented
        return lhs.approx(rhs, rtol=UNIT_SCALE_RTOL)

    def __ne__(lhs, rhs):
        return not lhs == rhs

    def __lt__(SIUnit lhs not None, SIUnit rhs not None):
        return lhs.cmp(rhs) < 0

    def __le__(SIUnit lhs not None, SIUnit rhs not None):
        return lhs.cmp(rhs) <= 0

    def __gt__(SIUnit lhs not None, SIUnit rhs not None):
        return lhs.cmp(rhs) > 0

    def __ge__(SIUnit lhs not None, SIUnit rhs not None):
        return lhs.cmp(rhs) >= 0


    cpdef cmp(SIUnit self, SIUnit other):
        cdef int signum, error_code
        error_code = c.cmp_udata(signum, self.data, other.data)
        if error_code == c.Success:
            return signum

        if error_code == c.DimensionMismatch:
            raise ValueError("units mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    cpdef approx(SIUnit self, SIUnit other, double rtol=1e-9, double atol=0.0):
        if not self.compatible(other):
            raise ValueError("unit mismatch")
        return c.fapprox(self.data.scale, other.data.scale, rtol, atol)

    cpdef bint compatible(SIUnit self, SIUnit other):
        return c.eq_ddata(self.data.dimensions, other.data.dimensions)

    """
    Arithmetic Methods
    """

    def __mul__(lhs, rhs):
        cdef c.QData lhs_data, rhs_data
        cdef int operand_code
        operand_code = parse_uoperand(lhs_data, lhs) | parse_uoperand(rhs_data, rhs)
        if operand_code & c.OBJECT:
            return NotImplemented
        if operand_code & c.QUANTITY:
            return mul_quantities(lhs_data, rhs_data)
        return mul_units(lhs_data.units, rhs_data.units)


    def __truediv__(lhs, rhs):
        cdef c.QData lhs_data, rhs_data
        cdef int operand_code
        operand_code = parse_uoperand(lhs_data, lhs) | parse_uoperand(rhs_data, rhs)
        if operand_code & c.OBJECT:
            return NotImplemented
        if operand_code & c.QUANTITY:
            return div_quantities(lhs_data, rhs_data)
        return div_units(lhs_data.units, rhs_data.units)

    def __invert__(self):
        cdef c.Error error_code
        cdef SIUnit ret = SIUnit.__new__(SIUnit)
        ret.data.scale = 1.0
        ret.data.dimensions.exponents[:] = [0,0,0,0,0,0,0]
        error_code = c.div_udata(ret.data, ret.data, self.data)
        if error_code == c.Success:
            return ret

        if error_code == c.ZeroDiv:
            raise ZeroDivisionError()

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __pow__(lhs, rhs, modulo):
        if type(lhs) is not SIUnit:
            raise TypeError("Expected SIUnit ** Number")
        return lhs.exp(rhs)

    cpdef SIUnit exp(SIUnit self, double power):
        cdef c.Error error_code
        cdef SIUnit ret = SIUnit.__new__(SIUnit)
        error_code = c.pow_udata(ret.data, self.data, power)
        if error_code == c.Success:
            return ret

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return self

    def __hash__(self):
        data_tuple = (self.data.scale, tuple(self.data.dimensions.exponents))
        return hash(data_tuple)

    def __repr__(self):
        return 'SIUnit(%f, %r)' % (self.scale, self.dimensions)

cdef class Quantity:

    @property
    def quantity(self):
        return self.data.quantity

    @property
    def q(self):
        return self.data.quantity

    @property
    def units(self):
        cdef SIUnit units = SIUnit.__new__(SIUnit)
        units.data = self.data.units
        return units

    def __init__(Quantity self, double quantity, SIUnit units not None):
        self.data.quantity = quantity
        self.data.units = units.data

    cpdef is_of(Quantity self, d.Dimensions dims):
        if dims is None:
            raise TypeError()

        return c.eq_ddata(self.data.units.dimensions, dims.data)

    cpdef get_as(Quantity self, SIUnit units):
        if units is None:
            raise TypeError()

        cdef c.Error error_code
        cdef double value
        error_code = c.extract_quantity(value, self.data, units.data)
        if error_code == c.Success:
            return value

        if error_code == c.DimensionMismatch:
            raise ValueError("units mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    cpdef round_as(Quantity self, SIUnit units):
        return round(self.get_as(units))

    cpdef Quantity cvt_to(Quantity self, SIUnit units):
        if units is None:
            raise TypeError()

        cdef c.Error error_code
        cdef int cmp

        error_code = c.cmp_udata(cmp, self.data.units, units.data)
        if error_code == c.DimensionMismatch:
            raise ValueError("units mismatch")

        if cmp == 0:
            return self

        cdef Quantity ret = Quantity.__new__(Quantity)
        c.cvt_quantity(ret.data, self.data, units.data)
        return ret

    cpdef Quantity round_to(Quantity self, SIUnit units):
        if units is None:
            raise TypeError()

        cdef c.Error error_code
        cdef Quantity ret = Quantity.__new__(Quantity)

        error_code = c.cvt_quantity(ret.data, self.data, units.data)
        if error_code == c.Success:
            ret.data.quantity = round(ret.data.quantity)
            return ret

        if error_code == c.DimensionMismatch:
            raise ValueError("units mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    """
    Comparison Methods
    """

    def __eq__(lhs, rhs):
        if type(lhs) is not Quantity:
            return NotImplemented
        if type(rhs) is not Quantity:
            return NotImplemented

        try:
            return lhs.cmp(rhs) == 0
        except ValueError:
            return NotImplemented

    def __ne__(lhs, rhs):
        return not lhs == rhs

    def __lt__(Quantity lhs not None, Quantity rhs not None):
        return lhs.cmp(rhs) < 0

    def __le__(Quantity lhs not None, Quantity rhs not None):
        return lhs.cmp(rhs) <= 0

    def __gt__(Quantity lhs not None, Quantity rhs not None):
        return lhs.cmp(rhs) > 0

    def __ge__(Quantity lhs not None, Quantity rhs not None):
        return lhs.cmp(rhs) >= 0

    cpdef cmp(Quantity self, Quantity other):
        cdef int signum, error_code
        error_code = c.cmp_qdata(signum, self.data, other.data)
        if error_code == c.Success:
            return signum

        if error_code == c.DimensionMismatch:
            raise ValueError('unit mismatch')

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    cpdef bint compatible(Quantity self, Quantity other):
        return c.eq_ddata(self.data.units.dimensions, other.data.units.dimensions)

    cpdef r_approx(Quantity self, Quantity other, double rtol=1e-9):
        cdef int error_code
        cdef c.UData norm_udata
        cdef double self_norm, other_norm, epsilon

        error_code = c.min_udata(norm_udata, self.data.units, other.data.units)

        if error_code == c.Success:

            self_norm = c.unsafe_extract_quantity(self.data, norm_udata)
            other_norm = c.unsafe_extract_quantity(other.data, norm_udata)

            epsilon = fmax(1.0, fmax(self_norm, other_norm)) * rtol
            return fabs(self_norm - other_norm) <= fabs(epsilon)

        if error_code == c.DimensionMismatch:
            raise ValueError("unit mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    cpdef a_approx(Quantity self, Quantity other, double atol=1e-6):
        cdef int error_code
        cdef c.UData norm_udata
        cdef double self_norm, other_norm

        error_code = c.min_udata(norm_udata, self.data.units, other.data.units)
        if error_code == c.Success:
            self_norm = c.unsafe_extract_quantity(self.data, norm_udata)
            other_norm = c.unsafe_extract_quantity(other.data, norm_udata)
            return fabs(self_norm - other_norm) <= fabs(atol)

        if error_code == c.DimensionMismatch:
            raise ValueError("unit mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)


    cpdef q_approx(Quantity self, Quantity other, Quantity qtol):
        cdef int error_code1, error_code2
        cdef double self_val, other_val
        error_code1 = c.extract_quantity(self_val, self.data, qtol.data.units)
        error_code2 = c.extract_quantity(other_val, other.data, qtol.data.units)

        if error_code1 | error_code2 == c.Success:
            return fabs(self_val - other_val) <= fabs(qtol.data.quantity)

        if error_code1 == c.DimensionMismatch:
            raise ValueError("unit mismatch (lhs)")
        if error_code2 == c.DimensionMismatch:
            raise ValueError("unit mismatch (rhs)")

        raise RuntimeError("Unknown Error Occurred: %i" % (error_code1 | error_code2))

    """
    Arithmetic Methods
    """

    def __add__(Quantity lhs not None, Quantity rhs not None):
        cdef int error_code
        cdef Quantity ret = Quantity.__new__(Quantity)
        error_code = c.add_qdata(ret.data, lhs.data, rhs.data)
        if error_code == c.Success:
            return ret

        if error_code == c.DimensionMismatch:
            raise ValueError("unit mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __sub__(Quantity lhs not None, Quantity rhs not None):
        cdef int error_code
        cdef Quantity ret = Quantity.__new__(Quantity)
        error_code = c.sub_qdata(ret.data, lhs.data, rhs.data)
        if error_code == c.Success:
            return ret

        if error_code == c.DimensionMismatch:
            raise ValueError("unit mismatch")

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __mul__(lhs not None, rhs not None):
        cdef Quantity ret = Quantity.__new__(Quantity)
        cdef c.QData other
        cdef int operand_code, error_code
        operand_code = parse_qoperand(ret.data, lhs) | parse_qoperand(other, rhs)
        if operand_code & c.OBJECT:
            return NotImplemented

        error_code = c.mul_qdata(ret.data, ret.data, other)
        if error_code == c.Success:
            return ret

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __truediv__(lhs not None, rhs not None):
        cdef Quantity ret = Quantity.__new__(Quantity)
        cdef c.QData other
        cdef int operand_code, error_code
        operand_code = parse_qoperand(ret.data, lhs) | parse_qoperand(other, rhs)
        if operand_code & c.OBJECT:
            return NotImplemented
        error_code = c.div_qdata(ret.data, ret.data, other)
        if error_code == c.Success:
            return ret

        if error_code == c.ZeroDiv:
            raise ZeroDivisionError()

        return RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __pow__(lhs, rhs, modulo):
        if type(lhs) is not Quantity:
            raise TypeError("Expected Quantity ** Number")
        return lhs.exp(rhs)

    def __neg__(Quantity self):
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = -self.data.quantity
        ret.data.units = self.data.units
        return ret

    def __invert__(Quantity self):
        cdef int error_code
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = 1.0
        ret.data.units.scale = 1.0
        error_code = c.div_qdata(ret.data, ret.data, self.data)
        if error_code == c.Success:
            return ret

        if error_code == c.ZeroDiv:
            raise ZeroDivisionError()

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __abs__(Quantity self):
        if self.data.quantity >= 0:
            return self
        cdef Quantity ret = Quantity.__new__(Quantity)
        ret.data.quantity = fabs(self.data.quantity)
        ret.data.units = self.data.units
        return ret

    cpdef Quantity exp(Quantity self, double power):
        cdef int error_code
        cdef Quantity ret = Quantity.__new__(Quantity)
        error_code = c.pow_qdata(ret.data, self.data, power)
        if error_code == c.Success:
            return ret

        raise RuntimeError("Unknown Error Occurred: %i" % error_code)

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return self

    def __bool__(Quantity self):
        return bool(self.data.quantity)

    def __float__(Quantity self):
        return float(self.data.quantity)

    def __int__(Quantity self):
        return int(self.data.quantity)

    def __hash__(Quantity self):
        cdef double normalized = self.data.quantity * self.data.units.scale
        exponents = tuple(self.data.units.dimensions.exponents)
        qtuple = (normalized, exponents)
        return hash(qtuple)

    def __repr__(self):
        return 'Quantity(%f, %r)' % (self.quantity, self.units)