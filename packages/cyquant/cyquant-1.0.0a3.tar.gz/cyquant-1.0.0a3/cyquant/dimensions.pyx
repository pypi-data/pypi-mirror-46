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

#:
angle_t = Dimensions()

#:
solid_angle_t = Dimensions()

#:
strain_t = Dimensions()

#:
ratio_t = Dimensions()

#:
mass_t = Dimensions(kg=1)

#:
distance_t = Dimensions(m=1)

#:
time_t = Dimensions(s=1)

#:
temperature_t = Dimensions(k=1)

#:
current_t = Dimensions(a=1)

#:
amount_t = Dimensions(mol=1)

#:
luminosity_t = Dimensions(cd=1)

#:
frequency_t = Dimensions(s=-1)

#:
speed_t = distance_t / time_t

#:
acceleration_t = speed_t / time_t

#:
jerk_t = acceleration_t / time_t

#:
jounce_t = jerk_t / time_t

#:
area_t = distance_t ** 2

#:
volume_t = distance_t ** 3

#:
density_t = mass_t / volume_t

#:
volumetric_flow_t = volume_t / time_t

#:
force_t = mass_t * acceleration_t

#:
moment_t = force_t * distance_t

#:
torque_t = moment_t

#:
impulse_t = force_t * time_t

#:
momentum_t = impulse_t

#:
stress_t = force_t / area_t

#:
pressure_t = stress_t

#:
hydrostatic_pressure_t = density_t * acceleration_t * distance_t

#:
stiffness_t = force_t / distance_t

#:
surface_tension_t = stiffness_t

#:
energy_t = force_t * distance_t

#:
work_t = energy_t

#:
heat_t = energy_t

#:
power_t = energy_t / time_t

#:
charge_t = current_t * time_t

#:
potential_t = energy_t / current_t

#:
capacitance_t = charge_t / potential_t

#:
resistance_t = potential_t / current_t

#:
impedance_t = resistance_t

#:
reactance_t = resistance_t

#:
conductance_t = current_t / potential_t

#:
magnetic_flux_t = energy_t / current_t

#:
magnetic_flux_density_t = magnetic_flux_t / area_t

#:
inductance_t = impedance_t * time_t

#:
luminous_flux_t = luminosity_t * solid_angle_t

#:
illuminance_t = luminous_flux_t / area_t

#:
molarity_t = amount_t / volume_t

#:
molality_t = amount_t / mass_t

#:
molar_mass_t = mass_t / amount_t

#:
entropy_t = energy_t / temperature_t

#:
heat_capacity_t = entropy_t

#:
specific_entropy_t = entropy_t / mass_t

#:
specific_heat_capacity_t = specific_entropy_t

#:
temperature_gradient_t = temperature_t / distance_t