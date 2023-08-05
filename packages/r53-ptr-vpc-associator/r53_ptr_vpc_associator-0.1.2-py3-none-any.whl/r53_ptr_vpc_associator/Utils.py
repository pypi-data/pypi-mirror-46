"""
Utilities
"""
import logging
import traceback
import sys
import inspect
from botocore.exceptions import ClientError



LOGGER = logging.getLogger()


def lineno():  # pragma: no cover
    """
    Returns the current line number in our script
    :return: line number string
    """
    return str(' - Utils - line number: ' + str(inspect.currentframe().f_back.f_lineno))


class Utils(object):
    """
    Utils
    """

    def __init__(self, debug=False):
        self.debug = debug

        if self.debug:
            LOGGER.setLevel(logging.DEBUG)
        LOGGER.debug('Utils - init %s', lineno())

    def pretty(self, value, htchar='\t', lfchar='\n', indent=0):
        """
        Pretty json
        :param htchar:
        :param lfchar:
        :param indent:
        :param debug:
        :return:
        """
        LOGGER.debug("pretty %s", lineno())
        nlch = lfchar + htchar * (indent + 1)

        if type(value) is dict:
            items = [
                nlch + repr(key) + ': ' + self.pretty(value[key], htchar, lfchar, indent + 1)
                for key in value
            ]
            return '{%s}' % (','.join(items) + lfchar + htchar * indent)
        elif type(value) is list:
            items = [
                nlch + self.pretty(item, htchar, lfchar, indent + 1)
                for item in value
            ]
            return '[%s]' % (','.join(items) + lfchar + htchar * indent)
        elif type(value) is tuple:
            items = [
                nlch + self.pretty(item, htchar, lfchar, indent + 1)
                for item in value
            ]
            return '(%s)' % (','.join(items) + lfchar + htchar * indent)

        return repr(value)

    def get_client(self, session, name):
        """
        Get boto client
        :param name:
        :param debug:
        :return:
        """

        LOGGER.debug('get_client: %s %s', name, lineno())

        try:
            return session.client(service_name=str(name))
        except ClientError as err:
            LOGGER.warning("%s %s", str(err), lineno())
            raise err

    def get_hosted_zones(self, r53_client):
        """
        Get hosted zones
        :return:
        """

        LOGGER.debug('get_hosted_zones %s', lineno())
        resource_lists = []
        retry = True
        count = 0
        first_token = 'test'

        while retry:
            try:

                next_token = first_token

                while next_token:
                    if next_token == first_token:
                        response = r53_client.list_hosted_zones()
                    else:
                        response = r53_client.list_hosted_zones(
                            Marker=next_token
                        )

                    next_token = response.get('Marker', None)

                    for item in response['HostedZones']:
                        LOGGER.debug("item: %s %s", item, lineno())
                        # Only concerned with the reverse lookup zones
                        if 'addr.arpa' in item['Name']:
                            resource_lists.append(item)
                retry = False
            except Exception as wtf:
                count = count + 1
                LOGGER.error('list_hosted_zones({}) exploded: {}'.format(count, wtf))
                traceback.print_exc(file=sys.stderr)

        LOGGER.debug("resource_lists: %s %s", str(resource_lists), lineno())
        return resource_lists


    def associate_vpc_to_zone(self, r53_client, zone_id, vpc_id, vpc_region):
        """
        Associate vpc to zone
        :return:
        """

        LOGGER.debug("associate_vpc_to_zone %s", lineno())
        zone_id = zone_id.replace('/hostedzone/', '')
        LOGGER.debug("### zone id: %s %s", zone_id, lineno())

        try:

            r53_client.associate_vpc_with_hosted_zone(
                HostedZoneId=zone_id,
                VPC={
                    'VPCRegion': vpc_region,
                    'VPCId': vpc_id
                }
            )

            return

        except ClientError as e:
            LOGGER.warning("%s %s", str(e), lineno())
            raise e




    def get_zone_vpc_associations(self, r53_client, zone_id):
        """
        Get vpc associations
        :param r53_client:
        :param zone_id:
        :return:
        """

        LOGGER.debug("get_zone_vpc_associations %s", lineno())

        zone_id = zone_id.replace('/hostedzone/', '')
        LOGGER.debug('### zone id: %s', zone_id)

        try:
            response = r53_client.get_hosted_zone(
                Id=zone_id,
            )

            return response['VPCs']

        except ClientError as err:
            LOGGER.warning("%s %s", str(err), lineno())
            raise err
