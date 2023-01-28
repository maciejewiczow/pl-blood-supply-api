from pydantic import BaseModel
from api.models.DonationCenter import DonationCenter
from api.models.SupplyLevel import SupplyLevel

class DonationCenterSupply(BaseModel):
    donationCenter: DonationCenter
    supplyLevel: SupplyLevel
