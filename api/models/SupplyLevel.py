from enum import Enum, auto

class SupplyLevel(str, Enum):
    low = 'low'
    moderate = 'moderate'
    optimal = 'optimal'
    full = 'full'
    stop = 'stop'
    unknown = 'unknown'

    @staticmethod
    def parse(value: str):
        for key, enumVal in supplyLevelImageSrcs.items():
            if key in value:
                return enumVal

        return SupplyLevel.unknown

supplyLevelImageSrcs = {
    'krew3': SupplyLevel.low,
    'krew2': SupplyLevel.moderate,
    'krew1': SupplyLevel.optimal,
    'krew11': SupplyLevel.full,
    'krew0': SupplyLevel.stop,
}
