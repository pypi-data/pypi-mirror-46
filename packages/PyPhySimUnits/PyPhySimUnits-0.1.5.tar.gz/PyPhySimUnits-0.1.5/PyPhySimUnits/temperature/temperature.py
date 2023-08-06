from typing import Union

import numpy as np

from ..base import BaseQuantity


DEBUG = False


class Temperature(BaseQuantity):
    def __init__(self, system: str, name: str, value: Union[float, np.ndarray], to_base = None, from_base = None):
        super().__init__(system, name, 'Temperature', value, to_base, from_base)
        self.base = Kelvin

    def convert(self, new_unit: 'Temperature'):
        C_TO_K_PRECISION = 273.15

        if self.name == 'Kelvin':
            if new_unit == Celsius:
                return Celsius(self.value - C_TO_K_PRECISION)
            elif new_unit == Farenheit:
                return Farenheit((self.value - 273.15) * (9.0 / 5.0) + 32.0)

        elif self.name == 'Celsius':
            if new_unit == Kelvin:
                return Kelvin(self.value + C_TO_K_PRECISION)
            elif new_unit == Farenheit:
                return Farenheit((self.value) * (9.0 / 5.0) + 32.0)

        elif self.name == 'Farenheit':
            if new_unit == Celsius:
                return Celsius((self.value - 32.0) * (5.0 / 9.0))
            elif new_unit == Kelvin:
                return Kelvin(((self.value - 32.0) * (5.0 / 9.0)) + C_TO_K_PRECISION)

        if DEBUG:
            print(f'No suitable conversion class found for {self.name} to {new_unit}')
        return self


class Kelvin(Temperature):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('SI', 'Kelvin', value)


class Celsius(Temperature):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Metric', 'Celsius', value)


class Farenheit(Temperature):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Imperial', 'Farenheit', value)


if __name__ == '__main__':
    t = Kelvin(273.15)
    print(t)
    t = t.convert(Celsius)
    print(t)
    t = t.convert(Farenheit)
    print(t)
    t = t.convert(Kelvin)
    print(t)
    t = t.convert('garbage')
    print(t)
