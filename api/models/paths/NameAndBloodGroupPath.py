from api.models.paths.BasePath import BasePath

class NameAndBloodGroupPath(BasePath):
    donationCenter: str
    bloodGroup: str
