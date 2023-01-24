from email.policy import strict
from pydantic import BaseModel

class DonationCenter(BaseModel):
    name: str
    streetAddress: str
    postalCode: str
    city: str
    phoneNumber: str
    websiteUrl: str
