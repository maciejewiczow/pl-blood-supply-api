from typing import Any
from pydantic import BaseModel
from api.models.BloodRhD import BloodRhD
from api.models.BloodType import BloodType

class BloodGroup(BaseModel):
    groupString: str
    type: BloodType
    RhD: BloodRhD

    def __init__(self, groupString: str) -> None:
        super().__init__(
            groupString=groupString,
            type=BloodType.parse(groupString),
            RhD=BloodRhD.parse(groupString)
        )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, BloodGroup):
            return self.groupString == other.groupString

        return super().__eq__(other)

