#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2","snowflake-connector-python","boto3","pandas"]

setup(
    name="ohmylamb",
    version="0.0.1",
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
