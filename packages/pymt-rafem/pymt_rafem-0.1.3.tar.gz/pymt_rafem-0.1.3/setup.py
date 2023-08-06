#! /usr/bin/env python
import os
import sys
import versioneer
from setuptools import find_packages, setup

from model_metadata.utils import get_cmdclass, get_entry_points


packages = find_packages()
pymt_components = [
    (
        "Rafem=pymt_rafem.bmi:Rafem",
        "meta/Rafem",
    ),
]


setup(
    name="pymt_rafem",
    author="Eric Hutton",
    description="PyMT plugin rafem",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    version=versioneer.get_version(),
    long_description=open("README.rst").read(),
    install_requires=["rafem"],
    packages=packages,
    cmdclass=versioneer.get_cmdclass(),
    entry_points=get_entry_points(pymt_components),
    include_package_data=True,
)
