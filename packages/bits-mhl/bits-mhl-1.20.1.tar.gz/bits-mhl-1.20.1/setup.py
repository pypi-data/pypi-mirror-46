# -*- coding: utf-8 -*-
"""Install bits-mhl."""
# Copyright 2018 Broad Institute of MIT and Harvard
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

VERSION = "1.20.1"


# This was a great idea!! https://github.com/levlaz/circleci.py/blob/master/setup.py
class VerifyVersionCommand(install):
    """Verify that the git tag matches our version."""
    description = "verify that the git tag matches our version"

    def run(self):
        """Check the CIRCLE_TAG environment variable against the recorded version."""
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(tag, VERSION)
            sys.exit(info)


setup(
    name='bits-mhl',

    version=VERSION,

    description='BITS MHL',
    long_description='',

    author='Lukas Karlsson',
    author_email='karlsson@broadinstitute.org',

    license='Apache Software License',

    packages=find_packages(),
    install_requires=[
        'netaddr',
    ],
    cmdclass={"verify": VerifyVersionCommand},
    zip_safe=False,
)
