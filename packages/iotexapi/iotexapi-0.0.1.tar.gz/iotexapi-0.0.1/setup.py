#!/usr/bin/env python

"""
    setup
    =====
"""

import os
import platform
from setuptools import (
    find_packages,
    setup,
)
import pathlib

py_version = platform.python_version()

PACKAGE_VERSION = '0.0.1'

EXTRAS_REQUIRE = {
    'tester': [
        'coverage',
        'pep8',
        'pyflakes',
        'pylint',
        'pytest-cov'
    ],

    'docs': [
        "mock",
        "sphinx-better-theme>=0.1.4",
        "click>=5.1",
        "configparser==3.5.0",
        "contextlib2>=0.5.4",
        "py-solc>=0.4.0",
        "pytest>=2.7.2",
        "sphinx",
        "sphinx_rtd_theme>=0.1.9",
        "toposort>=1.4",
        "urllib3",
        "iotexapi",
        "wheel"
    ],

    'dev': [
        "bumpversion",
        "flaky>=3.3.0",
        "hypothesis>=3.31.2",
        "pytest>=3.5.0,<4",
        "pytest-mock==1.*",
        "pytest-pythonpath>=0.3",
        "pytest-watch==4.*",
        "pytest-xdist==1.*",
        "setuptools>=36.2.0",
        "tox>=1.8.0",
        "tqdm",
        "when-changed"
    ]

}

EXTRAS_REQUIRE['dev'] = (
        EXTRAS_REQUIRE['tester'] +
        EXTRAS_REQUIRE['docs'] +
        EXTRAS_REQUIRE['dev']
)

install_requires = [
    "toolz>=0.9.0,<1.0.0;implementation_name=='pypy'",
    "cytoolz>=0.9.0,<1.0.0;implementation_name=='cpython'",

    "eth-abi>=2.0.0b6,<3.0.0",
    "eth-account>=0.2.1,<0.4.0",
    "eth-utils>=1.3.0,<2.0.0",
    "eth-hash[pycryptodome]>=0.2.0,<1.0.0",

    "bech32>=1.1.0",

    "google-api-core>=1.11.0",
    "grpcio>=1.20.1",

    "hexbytes>=0.1.0,<1.0.0",

    "requests>=2.16.0,<3.0.0",
    "base58",
    "ecdsa",
    'attrdict',
]

this_dir = os.path.dirname(__file__)
#readme_filename = os.path.join(this_dir, 'README.md')

#with open(readme_filename) as f:
#    PACKAGE_LONG_DESCRIPTION = f.read()

# The directory containing this file
HERE = pathlib.Path(__file__).parent
# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='iotexapi',
    version=PACKAGE_VERSION,
    description='A Python API for interacting with IoTeX',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='iotex iotex-api iotex-api-python',
    url='https://github.com/iotask/iotex-api-python',
    author='IoTASK',
    author_email='iotask@iotask.io',
    license='MIT License',
    zip_safe=False,
    python_requires='>=3.6,<4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=['examples']),
    include_package_data=True,
    install_requires=install_requires,
    tests_require=EXTRAS_REQUIRE['tester'],
    extras_require=EXTRAS_REQUIRE,
)
