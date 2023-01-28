from typing import List
import requests
from bs4 import BeautifulSoup, NavigableString
from api.models.DonationCenter import DonationCenter
from api.models.SupplyLevel import SupplyLevel
from api.models.BloodGroup import BloodGroup

from api.models.FullBloodSupplyDataPoint import FullBloodSupplyDataPoint
from api.models.responses.BloodGroupSupply import BloodGroupSupply
from api.models.responses.DonationCenterSupply import DonationCenterSupply

def getBloodSupplyList(url: str, donationCenters: List[DonationCenter]):
    res = requests.get(url)
    document = BeautifulSoup(res.content, 'html.parser')

    bloodSupplyTableElement = document.find('table')

    if bloodSupplyTableElement == None or isinstance(bloodSupplyTableElement, NavigableString):
        return None

    headers = bloodSupplyTableElement.select('thead tr th a')

    for row in bloodSupplyTableElement.select('tbody tr'):
        cells = row.find_all('td')
        bloodGroupStr = cells[0].text

        cellsIt = iter(zip(headers, cells))
        next(cellsIt)

        for header, cell in cellsIt:
            href = header['href']

            center = next(c for c in donationCenters if c.websiteUrl in href or c.websiteUrl.replace('www.', '') in href)
            yield FullBloodSupplyDataPoint(
                donationCenter=center,
                bloodGroup=BloodGroup(groupString=bloodGroupStr),
                supplyLevel=SupplyLevel.parse(cell.find('img')['src'])
            )

def getBloodSupplyByCenterName(name: str, url: str, donationCenters: List[DonationCenter]):
    return (
        BloodGroupSupply(
            bloodGroup=s.bloodGroup,
            supplyLevel=s.supplyLevel
        ) for s in getBloodSupplyList(url, donationCenters) if s.donationCenter.name == name
    )

def getBloodSupplyByBloodGroup(bloodGroupString: str, url: str, donationCenters: List[DonationCenter]):
    group = BloodGroup(groupString=bloodGroupString)

    return (
        DonationCenterSupply(
            donationCenter=s.donationCenter,
            supplyLevel=s.supplyLevel
        ) for s in getBloodSupplyList(url, donationCenters) if s.bloodGroup == group
    )

def getBloodSupplyByCenterAndBloodGroup(centerName: str, bloodGroup: str, url: str, donationCenters: List[DonationCenter]):
    try:
        return next(
            s.supplyLevel for s in getBloodSupplyByCenterName(url=url, name=centerName, donationCenters=donationCenters) if s.bloodGroup.groupString == bloodGroup
        )
    except StopIteration:
        return None