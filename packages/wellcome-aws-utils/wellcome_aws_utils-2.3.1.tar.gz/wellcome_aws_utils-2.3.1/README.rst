aws_utils
=========

This module is a collection of AWS-related utilities that we wrote while working on the Wellcome Digital Platform.

Some of these utilities are very specific to Wellcome projects, others are more generic and should be generally useful.

Documentation is available at `wellcome-aws-utils.readthedocs.io <https://wellcome-aws-utils.readthedocs.io/en/latest/>`_.

Installation
************

You can install wellcome_aws_utils from PyPI::

   $ pip install wellcome_aws_utils

Note that this package **only supports Python 3.6 or later.**
It was originally written to run inside the AWS Lambda environment, which supports 2.7 or 3.6 --- and we make heavy use of f-strings, which are 3.6 only.

Running Tests
*************

First, run `export ROOT=$(git rev-parse --show-toplevel)`

To run tests, run `make test`

Additional requirements should be added to `setup.py`. Adding requirements may require removal of the local `.tox` directory - run `rm -rf .tox`

License
*******

MIT.
