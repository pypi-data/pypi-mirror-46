import unittest
import logging
import boto3
from mock import patch
from moto import mock_iam
from r53_ptr_vpc_associator.Utils import Utils
from r53_ptr_vpc_associator.Associator import Associator


logging.basicConfig(level=logging.DEBUG)

class TestUtils(unittest.TestCase):

    @mock_iam
    @patch('r53_ptr_vpc_associator.Utils.Utils.get_hosted_zones')
    @patch('r53_ptr_vpc_associator.Utils.Utils.get_zone_vpc_associations')
    def test_list_hosted_zones(self, associations, get_hosted_zones):

        get_hosted_zones.return_value = [{'Id': '/hostedzone/83531HW5IMBPTW4', 'Name': 'test.b.addr.arpa.', 'Config': {'Comment': 'test com', 'PrivateZone': True}, 'ResourceRecordSetCount': 0}, {'Id': '/hostedzone/2ZBWHBVXZWPMI5Z', 'Name': 'test.a.addr.arpa.', 'Config': {'Comment': 'test org', 'PrivateZone': True}, 'ResourceRecordSetCount': 0}]

        associations.return_value = [
            {
                'VPCRegion': 'us-east-1',
                'VPCId': 'vpc-d2faf8ba'
            }
        ]

        my_class = Associator(profile_name='default')

        response = my_class.list_hosted_zones()


        assert response == {'/hostedzone/2ZBWHBVXZWPMI5Z': [{'VPCId': 'vpc-d2faf8ba', 'VPCRegion': 'us-east-1'}], '/hostedzone/83531HW5IMBPTW4': [{'VPCId': 'vpc-d2faf8ba', 'VPCRegion': 'us-east-1'}]}

    @mock_iam
    @patch('r53_ptr_vpc_associator.Utils.Utils.associate_vpc_to_zone')
    @patch('r53_ptr_vpc_associator.Associator.list_hosted_zones')
    def test_associate_zones_to_vpc(self, zones, association):

        #zones.return_value = {'/hostedzone/2ZBWHBVXZWPMI5Z': [{'VPCId': 'vpc-d2faf8ba', 'VPCRegion': 'us-east-1'}], '/hostedzone/83531HW5IMBPTW4': [{'VPCId': 'vpc-d2faf8ba', 'VPCRegion': 'us-east-1'}]}
        zones.return_value = {'/hostedzone/2ZBWHBVXZWPMI5Z': [],
                              '/hostedzone/83531HW5IMBPTW4': []}

        association.return_value = None

        my_class = Associator(profile_name='default', debug=False, vpc_id='vpc-d2faf8ba', vpc_region='us-east-1')

        response = my_class.associate_zones_to_vpc()


        for item in response:

            if item != 'Successfully associated zone: /hostedzone/2ZBWHBVXZWPMI5Z with vpc: vpc-d2faf8ba':
                if item != 'Successfully associated zone: /hostedzone/83531HW5IMBPTW4 with vpc: vpc-d2faf8ba':
                    assert item == 'test'
