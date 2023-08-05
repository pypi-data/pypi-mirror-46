"""
Associator
"""
from __future__ import absolute_import, division, print_function
import logging
import inspect
import boto3
from r53_ptr_vpc_associator.Utils import Utils

LOGGER = logging.getLogger()


def lineno():
    """Returns the current line number in our program."""
    return str(' - Associator - line number: '+str(inspect.currentframe().f_back.f_lineno))


class Associator:
    """
    Creates an Associator object
    """

    def __init__(self, profile_name, debug=False, vpc_id=None, vpc_region=None):
        """
        Initialize Associator
        :param profile_name:
        :param debug:
        :param vpc_id:
        :param vpc_region:
        """
        self.debug = debug
        self.vpc_id = None
        self.vpc_region = None
        self.profile_name = profile_name
        self.utility = Utils(debug=self.debug)

        if self.profile_name.lower() == 'lambda':
            session = boto3.session.Session()
        else:
            session = boto3.session.Session(profile_name=self.profile_name)
        self.client = self.utility.get_client(session, 'route53')

        if self.debug:
            LOGGER.setLevel(logging.DEBUG)

        if vpc_id:
            self.vpc_id = vpc_id

        if vpc_region:
            self.vpc_region = vpc_region

    def associate_zones_to_vpc(self, pretty=False):
        """
        Associate zones to vpc
        :return:
        """


        zones = self.list_hosted_zones()

        results = []

        for zone in zones:
            LOGGER.debug("zone: %s %s %s", zone, str(zones[zone]), lineno())

            already_exists = False
            for vpcs in zones[zone]:
                if vpcs['VPCId'] == self.vpc_id:
                    already_exists = True

            if not already_exists:
                self.utility.associate_vpc_to_zone(self.client, zone, self.vpc_id, self.vpc_region)

                results.append('Successfully associated '
                               'zone: '+str(zone)+' with vpc: '+str(self.vpc_id))
            else:
                results.append('Not creating - an association '
                               'already exists between '
                               'zone: '+str(zone)+' and vpc: '+str(self.vpc_id))

        if pretty:
            return self.utility.pretty(results)

        return results

    def list_hosted_zones(self, pretty=False):
        """
        List hosted zones
        :param pretty:
        :return:
        """

        results = self.utility.get_hosted_zones(self.client)

        zones = {}

        # Iterate over hosted zones
        for item in results:
            LOGGER.debug("id: %s %s", str(item['Id']), lineno())
            results = self.utility.get_zone_vpc_associations(self.client, item['Id'])

            LOGGER.debug("zone results: %s %s",str(results), lineno())
            zones[item['Id']] = results

        if pretty:
            return self.utility.pretty(zones)

        return zones
