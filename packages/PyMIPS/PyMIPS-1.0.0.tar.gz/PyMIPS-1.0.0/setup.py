#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="PyMIPS",
    license="MIT",
    version="1.0.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AshtonUPS/Py-MI-PS",
    description="A python MIPS interpreter",
    author="Ashton Walden & Jiman Kim",
    author_email="awalden@pugetsound.edu",
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["tests"]),
    include_package_data=True,
    entry_points={"console_scripts": ["pymips = PyMIPS.__main__:main"]},
)
