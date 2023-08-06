cimport cyquant.ctypes as c

cimport cyquant.dimensions as d
import cyquant.dimensions as d

cimport cyquant.quantities as q
import cyquant.quantities as q

from functools import partial


def converter(q.SIUnit units not None, bint promotes=False):
    impl = _promiscuous_convert if promotes else _strict_convert
    return partial(impl, units)

def _strict_convert(q.SIUnit units not None, q.Quantity quantity not None):
    return quantity.cvt_to(units)

def _promiscuous_convert(q.SIUnit units not None, object value):
    if type(value) is q.Quantity:
        return value.cvt_to(units)

    # raises TypeError
    return q.Quantity(value, units)

def validator(d.Dimensions dims not None):
    return partial(are_of, dims)

def args_of(d.Dimensions dims not None, *qargs):
    return are_of(dims, qargs)

def are_of(d.Dimensions dims not None, qiterable):
    return all(q.is_of(dims) for q in qiterable)
