#!/bin/bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
echo "SCRIPTPATH: ${SCRIPTPATH}"
cd /tmp
if [ -d r53_ptr_vpc_associator ]; then rm -rf 53_ptr_vpc_associator; fi
mkdir r53_ptr_vpc_associator
cd r53_ptr_vpc_associator
mkdir code
cd code
pip install r53-ptr-vpc-associator -t .
#cp $SCRIPTPATH/lambda_example.py /tmp/r53_ptr_vpc_associator/code/lambda_function.py
zip -r /tmp/r53_ptr_vpc_associator/LambdaDeploymentPackage.zip .
echo "################################################################################"
echo "Zip package located at: /tmp/r53_ptr_vpc_associator/LambdaDeploymentPackage.zip"
echo "################################################################################"



