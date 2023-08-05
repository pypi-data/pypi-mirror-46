
r53_ptr_vpc_associator
======================

This is a program to association reverse zones to vpcs.  It is associated with https://github.com/aws-samples/aws-lambda-ddns-function

Installation
============

For general usage:

.. code-block::

   pip install r53_ptr_vpc_associator


For local development:

.. code-block::

   git clone https://github.com/rubelw/r53_ptr_vpc_associator
   cd r53_ptr_vpc_associator
   pip install --editable .  # Install the local dir as a package, including the 'dev' extras


Example
=======

Getting help

.. code-block::

   $ associator --help
   Usage: associator [OPTIONS] COMMAND [ARGS]...

   Options:
     --version  Show the version and exit.
     --help     Show this message and exit.

   Commands:
     associate  Associated hosted zones to vpc
     zone-list  List vpcs for hosted zones


Listing current zone/vpc associations

.. code-block::

   $ associator zone-list --profile-name default
   {
           '/hostedzone/Z1H1CDD4PZKKPB': [
           {
               'VPCRegion': 'us-east-1',
               'VPCId': 'vpc-99999999'
           },
           {
               'VPCRegion': 'us-east-2',
               'VPCId': 'vpc-99999999'
           }
       ]
   }


Associating zones

.. code-block::

   $ associator associate --profile-name default --vpc-id vpc-99999999  --vpc-region us-east-2
   [
       'Successfully associated zone: /hostedzone/A3G1CDD4PZKKPB with vpc: vpc-99999999',
       'Successfully associated zone: /hostedzone/HR2F2BVHDW5UD with vpc: vpc-99999999',
       'Successfully associated zone: /hostedzone/V6B06KVZ0ZL9U5 with vpc: vpc-99999999',
       'Successfully associated zone: /hostedzone/D7JTQ7EDFFYOWN with vpc: vpc-99999999'
   ]


Testing
^^^^^^^

Before commiting changes, be sure to run the test suite:

.. code-block::

   tox


Python 3 Compatibility
^^^^^^^^^^^^^^^^^^^^^^

This tool is compatible with **python 3.5+**.

The `tox <http://tox.readthedocs.io/en/latest/index.html>`_ library is used to run tests with multiple python versions. To run these tests, first ensure that all supported python versions are installed locally. Then, simply run:

.. code-block::

   tox
