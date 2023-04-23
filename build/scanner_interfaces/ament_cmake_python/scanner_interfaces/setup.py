from setuptools import find_packages
from setuptools import setup

setup(
    name='scanner_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('scanner_interfaces', 'scanner_interfaces.*')),
)
