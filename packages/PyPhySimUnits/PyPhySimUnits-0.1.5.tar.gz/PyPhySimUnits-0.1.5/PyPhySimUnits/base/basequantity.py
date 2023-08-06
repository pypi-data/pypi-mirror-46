from typing import List, Union, Type

import numpy as np

from ..util import COMPATIBILITY_MAPPING_REV


class Quantity(float):
    def __init__(self, value: Union[float, np.ndarray], name: str, meas_type: str):
        self.value = value
        self.name = name
        self.meas_type = meas_type
        super().__init__()

    def _check_units(self, other: 'Quantity') -> int:
        if self.name == other.name:
            return COMPATIBILITY_MAPPING_REV['Same Unit Type'] # 1
        elif self.meas_type == other.meas_type:
            return COMPATIBILITY_MAPPING_REV['Same Measurement Type, Differing Units'] # 2
        else:
            return COMPATIBILITY_MAPPING_REV['Different Measurement Types'] # 0

    def _pre_math_unit_check(self, other: 'Quantity') -> 'Quantity':
        compatible = self._check_units(other)
        if compatible == 0:
            # incompatible units
            '''
            TODO: define something like a 'UnknownQuantity' class that to cast this as. This way we
            continue calculations, store the original unit types as some attribute there, and see
            what two Quantity types were used.
            '''
            print(f'Unit types {self.__repr__()} & {other.__repr__()} incompatible. Not attempting conversion')
            return other
        elif compatible == 1:
            # compatible
            return other
        elif compatible == 2:
            # compatible, but need a conversion
            return other.convert(type(self))
        else:
            print('\n\nSomething has gone wrong\n\n')
            return None

    def _call_math_func(self, other):
        if isinstance(other, Quantity):
            return self._pre_math_unit_check(other)
        else:
            return other

    def _cast_as_same_unit(self, arg):
        return type(self)(arg)

    # Binary Operators: https://www.python-course.eu/python3_magic_methods.php
    def __add__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__add__(o))

    def __radd__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__radd__(o))

    def __sub__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__sub__(o))

    def __rsub__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__rsub__(o))

    def __mul__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__mul__(o))

    def __rmul__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__rmul__(o))

    def __floordiv__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__floordiv__(o))

    def __rfloordiv__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__rfloordiv__(o))

    def __truediv__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__truediv__(o))

    def __rtruediv__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__rtruediv__(o))

    def __mod__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__mod__(o))

    def __rmod__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__rmod__(o))

    def __pow__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__pow__(o))

    def __rpow__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__rpow__(o))

    # Extended assignments
    def __iadd__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__iadd__(o))

    def __isub__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__isub__(o))

    def __imul__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__imul__(o))

    def __idiv__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__idiv__(o))

    def __ifloordiv__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__ifloordiv__(o))

    def __imod__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__imod__(o))

    def __ipow__(self, other):
        o = self._call_math_func(other)
        return self._cast_as_same_unit(super().__ipow__(o))

    def __neg__(self):
        return self._cast_as_same_unit(super().__neg__())

    def __pos__(self):
        return self._cast_as_same_unit(super().__pos__())

    def __abs__(self):
        return self._cast_as_same_unit(super().__abs__())

    # Comparison operators
    def __lt__(self, other):
        o = self._call_math_func(other)
        return super().__lt__(o)

    def __le__(self, other):
        o = self._call_math_func(other)
        return super().__le__(o)

    def __eq__(self, other):
        o = self._call_math_func(other)
        return super().__eq__(o)

    def __ne__(self, other):
        o = self._call_math_func(other)
        return super().__ne__(o)

    def __ge__(self, other):
        o = self._call_math_func(other)
        return super().__ge__(o)

    def __gt__(self, other):
        o = self._call_math_func(other)
        return super().__gt__(o)


class BaseQuantity(Quantity):
    def __init__(self,
                 system: str,
                 name: str,
                 meas_type: str,
                 value: Union[float, np.ndarray],
                 to_base: float,
                 from_base: float):
        super().__init__(value, name, meas_type)
        self.system = system
        self._conv_to_base = to_base
        self._conv_from_base = from_base

    def __repr__(self):
        return f'{self.meas_type} object for {self.system} unit system: {self.name}'

    def __str__(self):
        return f'{self.value} {self.name} [{self.system}]'

    def convert(self, new_unit: 'BaseQuantity'):
        value = self.value * self._conv_to_base
        new_inst = new_unit(value)
        assert (self.meas_type == new_inst.meas_type), \
            f'Cannot convert from {self.meas_type} to {new_inst.meas_type}'
        new_inst.value = new_inst.value * new_inst._conv_from_base
        return new_inst


class DerivedQuantity(Quantity):
    def __init__(self,
                 name: str,
                 meas_type: str,
                 numerator: List[Union[BaseQuantity, 'DerivedQuantity']],
                 denominator: List[Union[BaseQuantity, 'DerivedQuantity']],
                 value: Union[float, np.ndarray]):
        super().__init__(value, name, meas_type)
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self):
        return f'{self.meas_type} of {self.value} {self.name}'

    def __str__(self):
        return f'{self.meas_type} of {self.value} {self.name}'

    def convert(self, new_unit: 'DerivedQuantity'):
        new_val = self.value
        unit = new_unit(1)
        for n1, n2 in zip(self.numerator, unit.numerator):
            t = n1(new_val)
            t = t.convert(n2)
            new_val = t.value

        for d1, d2 in zip(self.denominator, unit.denominator):
            t = d2(new_val)
            t = t.convert(d1)
            new_val = t.value

        return new_unit(new_val)
