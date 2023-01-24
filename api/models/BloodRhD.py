from enum import Enum, auto
import re

class BloodRhD(str, Enum):
    negative = 'negative'
    positive = 'positive'

    @staticmethod
    def parse(value: str):
        if re.search(r'(?i)Rh-', value):
            return BloodRhD.negative

        if re.search(r'(?i)Rh\+', value):
            return BloodRhD.positive

        raise ValueError(f'Unrecognized blood rhd type: "{value}"')
