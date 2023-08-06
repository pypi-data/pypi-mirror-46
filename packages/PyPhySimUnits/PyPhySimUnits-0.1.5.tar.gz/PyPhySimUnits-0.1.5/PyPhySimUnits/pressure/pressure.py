from typing import List

from ..base import DerivedQuantity
from .. import force
from .. import area


class Pressure(DerivedQuantity):
    def __init__(self,
                 name: str,
                 numerator: List[force.Force],
                 denominator: List[area.Area],
                 value: float):
        super().__init__(name, 'Pressure', numerator, denominator, value)
        self.base = Pascal


class Pascal(Pressure):
    def __init__(self, value: float):
        super().__init__('Pascal', [force.Newton], [area.MetersSquared], value)


class PSI(Pressure):
    def __init__(self, value: float):
        super().__init__('PSI', [force.PoundForce], [area.InchesSquared], value)
