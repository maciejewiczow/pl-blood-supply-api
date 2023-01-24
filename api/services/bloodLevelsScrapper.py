from typing import List
import requests
from bs4 import BeautifulSoup, NavigableString
from api.models.DonationCenter import DonationCenter
from api.models.SupplyLevel import SupplyLevel
from api.models.BloodGroup import BloodGroup
from api.models.BloodRhD import BloodRhD
from api.models.BloodSupplyDataPoint import BloodSupplyDataPoint
from api.models.BloodType import BloodType

def getBloodSupplyList(url: str, donationCenters: List[DonationCenter]) -> List[BloodSupplyDataPoint]:
    res = requests.get(url)
    document = BeautifulSoup(res.content, 'html.parser')

    bloodSupplyTableElement = document.find('table')

    if bloodSupplyTableElement == None or isinstance(bloodSupplyTableElement, NavigableString):
        return []

    headers = bloodSupplyTableElement.select('thead tr th a')

    results: List[BloodSupplyDataPoint] = []

    for row in bloodSupplyTableElement.select('tbody tr'):
        cells = row.find_all('td')
        bloodGroupStr = cells[0].text

        cellsIt = iter(zip(headers, cells))
        next(cellsIt)

        for header, cell in cellsIt:
            href = header['href']

            center = next(c for c in donationCenters if c.websiteUrl in href or c.websiteUrl.replace('www.', '') in href)

            results.append(
                BloodSupplyDataPoint(
                    donationCenter=center,
                    bloodGroup=BloodGroup(
                        type=BloodType.parse(bloodGroupStr),
                        RhD=BloodRhD.parse(bloodGroupStr)
                    ),
                    supplyLevel=SupplyLevel.parse(cell.find('img')['src'])
                )
            )

    return results
