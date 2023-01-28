from pydantic import BaseModel
from api.models.BloodGroup import BloodGroup
from api.models.SupplyLevel import SupplyLevel

class BloodGroupSupply(BaseModel):
    bloodGroup: BloodGroup
    supplyLevel: SupplyLevel
