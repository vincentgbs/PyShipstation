import os
from setuptools import setup, find_packages

# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "shipstation",
    version = "0.1.1",
    
    packages=find_packages(),
    package_data = {'' : ['README.txt']},
    install_requires = [],
    author = "vincent hu",
    author_email = None,
    description = "Connect Python applications with the ShipStation API",
    license = None,
    keywords = "shipstation api client",
    url = "https://github.com/vincentgbs/PyShipstation",
    
    long_description=read('README.txt'),
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2"
    ],
)
