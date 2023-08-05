#!/usr/bin/env python

# Copyright 2017 Canonical Ltd.
# Licensed under the LGPLv3, see LICENCE file for details.
import sys
import platform

from setuptools import (
    find_packages,
    setup,
)


PROJECT_NAME = 'macaroonbakery'

# version 1.2.3
VERSION = (1, 2, 3)


def get_version():
    '''Return the macaroon bakery version as a string.'''
    return '.'.join(map(str, VERSION))


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'requests>=2.18.1,<3.0',
    'PyNaCl>=1.1.2,<2.0',
    'pymacaroons>=0.12.0,<1.0',
    'six>=1.11.0,<2.0',
    'protobuf>=3.0.0,<4.0',
    'pyRFC3339>=1.0,<2.0',
]

test_requirements = [
    'tox',
    'httmock==1.2.5',
]

distribution = platform.dist()
if len(distribution) == 3 and distribution[2] == 'trusty':
    # Injected into urllib3 to fix insecure Python 2.
    requirements.extend([
        'cryptography==1.3.2',
        'pyOpenSSL==16.0.0',
        'pyasn1==0.1.9',
        'ndg_httpsclient==0.3.3',
    ])

if sys.version_info.major == 2:
    requirements.append('ipaddress')


setup(
    name=PROJECT_NAME,
    version=get_version(),
    description='A Python library port for bakery, higher level operation '
                'to work with macaroons',
    long_description=readme,
    author="Juju UI Team",
    author_email='juju-gui@lists.ubuntu.com',
    url='https://github.com/go-macaroon-bakery/py-macaroon-bakery',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="LGPL3",
    zip_safe=False,
    keywords='macaroon cookie',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
