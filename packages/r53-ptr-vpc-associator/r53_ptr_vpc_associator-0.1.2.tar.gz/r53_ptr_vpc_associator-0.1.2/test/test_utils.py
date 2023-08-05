import unittest
import logging
import boto3
from mock import patch
from moto import mock_route53, mock_route53_deprecated
from r53_ptr_vpc_associator.Utils import Utils


logging.basicConfig(level=logging.DEBUG)

class TestUtils(unittest.TestCase):


    def test_pretty(self):

        my_class = Utils()
        test = {
            'test':'test'
        }
        response = my_class.pretty(test)
        assert response == "{\n\t'test': 'test'\n}"


    @mock_route53
    def test_get_hosted_zones_without_arpa_in_name(self):
        client = boto3.client('route53', region_name='us-east-1')
        client.create_hosted_zone(
            Name="test.b.com.",
            CallerReference=str(hash('foo')),
            HostedZoneConfig=dict(
                PrivateZone=True,
                Comment="test com",
            )
        )
        client.create_hosted_zone(
            Name="test.a.org.",
            CallerReference=str(hash('bar')),
            HostedZoneConfig=dict(
                PrivateZone=True,
                Comment="test org",
            )
        )
        client.create_hosted_zone(
            Name="test.a.org.",
            CallerReference=str(hash('bar')),
            HostedZoneConfig=dict(
                PrivateZone=True,
                Comment="test org 2",
            )
        )

        my_class = Utils()

        response = my_class.get_hosted_zones(client)

        assert response == []

    @mock_route53
    def test_get_hosted_zones_with_arpa_in_name(self):
        client = boto3.client('route53', region_name='us-east-1')
        client.create_hosted_zone(
            Name="test.b.addr.arpa.",
            CallerReference=str(hash('foo')),
            HostedZoneConfig=dict(
                PrivateZone=True,
                Comment="test com",
            )
        )
        client.create_hosted_zone(
            Name="test.a.addr.arpa.",
            CallerReference=str(hash('bar')),
            HostedZoneConfig=dict(
                PrivateZone=True,
                Comment="test org",
            )
        )
        my_class = Utils()

        response = my_class.get_hosted_zones(client)

        has_test_a = False
        has_test_b = False


        for resp in response:
            if resp['Name'] == 'test.a.addr.arpa.':
                has_test_a = True
            elif resp['Name'] == 'test.b.addr.arpa.':
                has_test_b = True

        assert has_test_a == True
        assert has_test_a == True