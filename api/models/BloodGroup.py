from pydantic import BaseModel
from api.models.BloodRhD import BloodRhD
from api.models.BloodType import BloodType

class BloodGroup(BaseModel):
    type: BloodType
    RhD: BloodRhD
