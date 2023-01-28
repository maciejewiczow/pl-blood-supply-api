from typing import List
import requests
import csv

from api.models.DonationCenter import DonationCenter

brokenEncodingLetterReplacements = {
    '³': 'ł',
    'œ': 'ś',
    'æ': 'ć',
    'ñ': 'ń',
    'Ÿ': 'ź',
    '¯': 'Ż',
    '£': 'Ł',
    '¿': 'ż'
}

def getDonationCenters(listFileApiEndpoint: str):
    csvRes = requests.get(listFileApiEndpoint)

    csvText = csvRes.text
    for char, replacement in brokenEncodingLetterReplacements.items():
        csvText = csvText.replace(char, replacement)

    dataReader = csv.DictReader(csvText.splitlines(), delimiter=';')

    results: List[DonationCenter] = []
    for row in dataReader:
        name = row['RCKiK']
        streetAddress = row['Adres'].replace(',', '')
        postalCodeAndCity = row['kod pocztowy, miejscowość'].split(' ')
        postalCode = postalCodeAndCity[0]
        city = postalCodeAndCity[1]
        phoneNumber = row['telefon'].replace('tel. ', '')
        websiteUrl = row['strona internetowa']

        results.append(
            DonationCenter(
                name=name,
                streetAddress=streetAddress,
                postalCode=postalCode,
                city=city,
                phoneNumber=phoneNumber,
                websiteUrl=websiteUrl
            )
        )

    return results

def getDonationCenterByName(name: str, datasourceUrl: str):
    try:
        return next(dc for dc in getDonationCenters(datasourceUrl) if dc.name == name)
    except StopIteration:
        return None
