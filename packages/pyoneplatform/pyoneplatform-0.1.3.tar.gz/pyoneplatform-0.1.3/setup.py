# -*- coding: utf-8 -*-
from setuptools import setup
__version__ = '0.1.3'


def _long_description():
    with open('README.rst', 'r') as fd:
        long_description = fd.read()
    return long_description


setup(
    name="pyoneplatform",
    version=__version__,
    author="INET-SDI",
    author_email="inet-sdi@inet.co.th",
    maintainer="INET-SDI",
    maintainer_email="inet-sdi@inet.co.th",
    url="https://github.com/inetspa/oneplatform-sdk-python",
    description="OnePlatform API SDK for Python",
    long_description=_long_description(),
    license='GNU GPL 3.0',
    packages=[
        "oneplatform",
        "oneplatform.oneid"
    ],
    install_requires=[
        "requests",
    ],
)
