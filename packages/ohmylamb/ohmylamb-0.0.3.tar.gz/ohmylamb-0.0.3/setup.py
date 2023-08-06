#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["snowflake-connector-python","boto3","pandas"]

setup(
    name="ohmylamb",
    version="0.0.3",
    author="Rewati Raman",
    author_email="rewati.raman@allergan.com",
    description="A simple library to use AWS resources. And speedup development for lambda projects.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/rewatiraman/ohmylamb/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
)
