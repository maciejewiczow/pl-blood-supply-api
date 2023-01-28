from flask import jsonify
from flask_openapi3 import OpenAPI, Tag
from api.models.FullBloodSupplyDataPoint import FullBloodSupplyDataPoint
from api.models.DonationCenter import DonationCenter
from api.models.SupplyLevel import SupplyLevel, SupplyLevelModel
from api.models.paths.NameAndBloodGroupPath import NameAndBloodGroupPath
from api.models.paths.NamePath import NamePath
from api.models.responses.BloodGroupSupply import BloodGroupSupply
from api.models.responses.DonationCenterSupply import DonationCenterSupply
from api.models.responses.List import List
from api.services.donationCenters import getDonationCenterByName, getDonationCenters
from api.services.bloodLevelsScrapper import getBloodSupplyByBloodGroup, getBloodSupplyByCenterAndBloodGroup, getBloodSupplyByCenterName, getBloodSupplyList
import os

def defineEndpoints(app: OpenAPI):
    defineBloodSuplyEndpoints(app)
    defineDonationCenterEndpoints(app)

def defineBloodSuplyEndpoints(app: OpenAPI):
    bloodTag = Tag(name='Blood supply', description='Blood supply levels in Polish RCKiK facilities, scrapped from the [krew.info](https://krew.info/zapasy) website')
    donationCentersDataSourceUrl = os.environ['DONATION_CENTERS_LIST_FILE_URL']
    bloodSupplyDataSourceUrl = os.environ['BLOODBANK_WEBSITE_URL']

    @app.get(
        '/blood-supply',
        tags=[bloodTag],
        responses={
            "200": List[FullBloodSupplyDataPoint],
        }
    )
    def getBloodSupplyEndpoint():
        """ Get blood supply info for all facilities and blood groups
        Get all blood supply levels in every RCKiK in Poland, for every blood type
        """
        centers = getDonationCenters(donationCentersDataSourceUrl)
        return jsonify(list(getBloodSupplyList(bloodSupplyDataSourceUrl, centers))), 200

    @app.get(
        '/blood-supply/donation-center/<string:name>',
        tags=[bloodTag],
        responses={
            "200": List[BloodGroupSupply],
        }
    )
    def getBloodSupplyByCenterNameEndpoint(path: NamePath):
        """ Get blood supply in a specified donation center
        Get blood supply levels in a specified RCKiK donation center, for every blood type
        """

        centers = getDonationCenters(donationCentersDataSourceUrl)
        return jsonify(list(getBloodSupplyByCenterName(path.name, bloodSupplyDataSourceUrl, centers))), 200

    @app.get(
        '/blood-supply/blood-group/<string:name>',
        tags=[bloodTag],
        responses={
            "200": List[DonationCenterSupply],
        }
    )
    def getBloodSupplyByBloodGroupStringEndpoint(path: NamePath):
        """ Get blood supply of a specified blood group in different centers
        Get blood supply levels of a specified group type in different RCKiK centers
        """

        centers = getDonationCenters(donationCentersDataSourceUrl)
        return jsonify(list(getBloodSupplyByBloodGroup(path.name, bloodSupplyDataSourceUrl, centers))), 200

    @app.get(
        '/blood-supply/supply-level/<string:donationCenter>/<string:bloodGroup>',
        tags=[bloodTag],
        responses={
            "200": SupplyLevelModel,
        }
    )
    def getBloodSupplyByDonationCenterAndBloodGroupStringEndpoint(path: NameAndBloodGroupPath):
        """ Get blood supply of a specified blood group in a specified donation center
        Get blood supply levels of a specified group type in a specified RCKiK center
        """

        centers = getDonationCenters(donationCentersDataSourceUrl)
        result = getBloodSupplyByCenterAndBloodGroup(
            url=bloodSupplyDataSourceUrl,
            donationCenters=centers,
            bloodGroup=path.bloodGroup,
            centerName=path.donationCenter
        )

        if result == None:
            return '', 404

        return jsonify(result), 200


def defineDonationCenterEndpoints(app: OpenAPI):
    donationCenterTag = Tag(name='Donation centers', description='Data about Polish blood donation centers, acquired from the [Polish government api](https://api.dane.gov.pl)')
    datasourceUrl = os.environ['DONATION_CENTERS_LIST_FILE_URL']

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
        return jsonify(getDonationCenters(datasourceUrl)), 200

    @app.get(
        '/donation-centers/<string:name>',
        tags=[donationCenterTag],
        responses={
            '200': DonationCenter,
            '404': None
        }
    )
    def getDonationCenterByNameEndpoint(path: NamePath):
        """ Get single donation center by name """
        res = getDonationCenterByName(path.name, datasourceUrl)

        if res == None:
            return '', 404

        return jsonify(res), 200
