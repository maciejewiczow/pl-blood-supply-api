from enum import Enum, auto
import re

class BloodType(str, Enum):
    zero = 'zero'
    A = 'A'
    B = 'B'
    AB = 'AB'

    @staticmethod
    def parse(value: str):
        if re.search(r'^\s*0', value):
            return BloodType.zero

        if re.search(r'^\s*A ', value):
            return BloodType.A

        if re.search(r'^\s*B ', value):
            return BloodType.B

        if re.search(r'^\s*AB ', value):
            return BloodType.AB

        raise ValueError(f'Unrecognized blood type value "{value}"')
