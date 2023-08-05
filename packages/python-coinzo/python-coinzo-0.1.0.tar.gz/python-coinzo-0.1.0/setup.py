#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-coinzo",
    version="0.1.0",
    # scripts=["dokr"],
    author="tolgamorf",
    author_email="cryptolga@gmail.com",
    description="coinzo REST API python implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tolgamorf/python-coinzo",
    packages=["coinzo"],  # setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)


# install_requires=[
#     "requests",
#     "six",
#     "Twisted",
#     "pyOpenSSL",
#     "autobahn",
#     "service-identity",
#     "dateparser",
#     "urllib3",
#     "chardet",
#     "certifi",
#     "cryptography",
# ],
# keywords="coinzo exchange rest api bitcoin ethereum btc eth neo eos xrp hot",
