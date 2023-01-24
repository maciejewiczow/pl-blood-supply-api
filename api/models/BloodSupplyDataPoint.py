from pydantic import BaseModel
from api.models.DonationCenter import DonationCenter
from api.models.SupplyLevel import SupplyLevel
from api.models.BloodGroup import BloodGroup

class BloodSupplyDataPoint(BaseModel):
    donationCenter: DonationCenter
    bloodGroup: BloodGroup
    supplyLevel: SupplyLevel
