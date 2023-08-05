#!python
#cython: language_level=3

cimport cyquant.ctypes as c

cdef double DIMENSIONS_RTOL = 1e-12

cdef class Dimensions:

    @staticmethod
    def GetEqRelTol():
        return DIMENSIONS_RTOL

    @staticmethod
    def SetEqRelTol(double rtol):
        global DIMENSIONS_RTOL
        if rtol < 0:
            raise ValueError("relative tolerance must be greater than 0.")
        DIMENSIONS_RTOL = rtol

    @property
    def kg(self):
        return self.data.exponents[0]

    @property
    def m(self):
        return self.data.exponents[1]

    @property
    def s(self):
        return self.data.exponents[2]

    @property
    def k(self):
        return self.data.exponents[3]

    @property
    def a(self):
        return self.data.exponents[4]

    @property
    def mol(self):
        return self.data.exponents[5]

    @property
    def cd(self):
        return self.data.exponents[6]

    def __init__(Dimensions self, double kg=0, double m=0, double s=0, double k=0, double a=0, double mol=0, double cd=0):
        self.data.exponents[:] = [kg, m, s, k, a, mol, cd]

    def __mul__(Dimensions lhs, Dimensions rhs):
        cdef Dimensions ret_val = Dimensions.__new__(Dimensions)
        c.mul_ddata(ret_val.data, lhs.data, rhs.data)
        return ret_val

    def __truediv__(Dimensions lhs, Dimensions rhs):
        cdef Dimensions ret_val = Dimensions.__new__(Dimensions)
        c.div_ddata(ret_val.data, lhs.data, rhs.data)
        return ret_val

    def __pow__(lhs, rhs, modulo):
        if type(lhs) is not Dimensions:
            raise TypeError("Expected Dimensions ** Number")
        return lhs.exp(rhs)

    def __eq__(self, other):
        if type(self) is not Dimensions:
            return NotImplemented
        if type(other) is not Dimensions:
            return NotImplemented
        return self.approx(other)

    cpdef bint approx(Dimensions self, Dimensions other):
        cdef int i
        for i in range(7):
            if not c.fapprox(self.data.exponents[i], other.data.exponents[i], DIMENSIONS_RTOL, 0):
                return False
        return True

    cpdef Dimensions exp(Dimensions self, double exp):
        cdef Dimensions ret_val = Dimensions.__new__(Dimensions)
        c.pow_ddata(ret_val.data, self.data, exp)
        return ret_val

    def __copy__(self):
        return self

    def __deepcopy__(self, memodict={}):
        return self

    def __hash__(self):
        etuple = (self.kg, self.m, self.s, self.k, self.a, self.mol, self.cd)
        return hash(etuple)

    def __repr__(self):
        return 'Dimensions(kg=%f, m=%f, s=%f, k=%f, a=%f, mol=%f, cd=%f)' % (
            self.kg, self.m, self.s, self.k, self.a, self.mol, self.cd
        )


dimensionless_t = Dimensions()
