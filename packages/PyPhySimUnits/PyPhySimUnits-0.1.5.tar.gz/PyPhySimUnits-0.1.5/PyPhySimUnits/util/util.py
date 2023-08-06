from typing import Optional


COMPATIBILITY_MAPPING = {
    0: 'Different Measurement Types',
    1: 'Same Unit Type',
    2: 'Same Measurement Type, Differing Units'
}

COMPATIBILITY_MAPPING_REV = {
    COMPATIBILITY_MAPPING[0]: 0,
    COMPATIBILITY_MAPPING[1]: 1,
    COMPATIBILITY_MAPPING[2]: 2
}


def units_match(unit1,
                unit2) -> int:
    if type(unit1) == type(unit2):
        return 1
    elif unit1.meas_type == unit2.meas_type:
        # Units are of the same type of measurement, but not the same units
        return 2
    else:
        return 0


def print_compatibility(compat: int) -> None:
    try:
        print(COMPATIBILITY_MAPPING[compat])
    except KeyError:
        print(f'Value entered ({compat}) is not defined as a compatibility status')
        print(f'Compatibility values are {[f"{k} = {v}" for k, v in COMPATIBILITY_MAPPING.items()]}')
