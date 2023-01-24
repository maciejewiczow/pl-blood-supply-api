from flask import jsonify
from flask_openapi3 import OpenAPI, Tag
from api.models.BloodSupplyDataPoint import BloodSupplyDataPoint
from api.models.DonationCenter import DonationCenter
from api.models.responses.List import List
from api.services.donationCenters import getDonationCenters
from api.services.bloodLevelsScrapper import getBloodSupplyList
import os

def defineBloodSuplyEndpoints(app: OpenAPI):
    bloodTag = Tag(name='Blood supply', description='Blood supply levels in Polish RCKiK facilities, scrapped from the [krew.info](https://krew.info/zapasy) website')

    @app.get(
        '/blood-supply',
        tags=[bloodTag],
        responses={
            "200": List[BloodSupplyDataPoint],
        }
    )
    def getBloodSupplyEndpoint():
        """ Get blood supply info for all facilities and blood groups
        Get all blood supply levels in every RCKiK in Poland, for every blood type
        """
        centers = getDonationCenters(os.environ['DONATION_CENTERS_LIST_FILE_URL'])
        return jsonify(getBloodSupplyList(os.environ['BLOODBANK_WEBSITE_URL'], centers)), 200

def defineDonationCenterEndpoints(app: OpenAPI):
    donationCenterTag = Tag(name='Donation centers', description='Data about Polish blood donation centers, acquired from the [Polish government api](https://api.dane.gov.pl)')

    @app.get(
        '/donation-centers',
        tags=[donationCenterTag],
        responses={
            '200': List[DonationCenter],
        }
    )
    def getDonationCentersEndpoint():
        """ List all blood donation centers in Poland
        Get data about all the blood donation centers in Poland
        """
        return getDonationCenters(os.environ['DONATION_CENTERS_LIST_FILE_URL']), 200

def defineEndpoints(app: OpenAPI):
    defineBloodSuplyEndpoints(app)
    defineDonationCenterEndpoints(app)

