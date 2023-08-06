#!/usr/bin/env python3
"""MY project"""
from setuptools import find_packages, setup

with open("README.md", "r") as fobj:
    long_description = fobj.read()

setup(name='pymfactorial',
      version='0.1',
      description="pym Factorial module.",
      long_description=long_description,
      platforms=["Linux"],
      author="Kushal Das",
      author_email="kushaldas@gmail.com",
      url="https://pymbook.readthedocs.io/en/latest/",
      license="MIT",
      packages=find_packages()
      )
