from typing import List, Union

import numpy as np

from ..base import BaseQuantity, DerivedQuantity
from .. import energy
from .. import mass
from .. import temperature as temp

class SpecificHeat(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[energy.Energy],
                 denominator: List[Union[mass.Mass, temp.Temperature]],
                 value: Union[float, np.ndarray]):
        super().__init__(name, 'Specific Heat', numerator, denominator, value)
        self.base = JoulesPerKgKelvin


class JoulesPerKgKelvin(SpecificHeat):
    def __init__(self, value: Union[float, np.ndarray]):
        super().__init__('Joules per Kg•Kelvin', [energy.Joule], [mass.Kilogram, temp.Kelvin], value)
        # TODO: special-case handling for units with temperatures, converting this to Celsius
        # instead of Kelvin shouldn't change values here, but the code will as currently written


if __name__ == '__main__':
    cp = JoulesPerKgKelvin(10)
    print(cp)
