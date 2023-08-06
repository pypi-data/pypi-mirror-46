#! /usr/bin/env python
import os
import sys
import versioneer
from setuptools import find_packages, setup

from distutils.extension import Extension





packages = find_packages()
entry_points = {
    "pymt.plugins": [
        "OverlandFlow=pymt_landlab.bmi:OverlandFlow",
        "Flexure=pymt_landlab.bmi:Flexure",
        "LinearDiffuser=pymt_landlab.bmi:LinearDiffuser",
        "ExponentialWeatherer=pymt_landlab.bmi:ExponentialWeatherer",
        "TransportLengthHillslopeDiffuser=pymt_landlab.bmi:TransportLengthHillslopeDiffuser",
        "Vegetation=pymt_landlab.bmi:Vegetation",
        "SoilMoisture=pymt_landlab.bmi:SoilMoisture",
        "FlowDirectorSteepest=pymt_landlab.bmi:FlowDirectorSteepest",
        "FlowRouter=pymt_landlab.bmi:FlowRouter",
        "FlowAccumulator=pymt_landlab.bmi:FlowAccumulator",
        "StreamPowerEroder=pymt_landlab.bmi:StreamPowerEroder",
        "FlowDirectorD8=pymt_landlab.bmi:FlowDirectorD8",
        "FlowDirectorDINF=pymt_landlab.bmi:FlowDirectorDINF",
    ]
}

cmdclass = versioneer.get_cmdclass()

setup(
    name="pymt_landlab",
    author="Eric Hutton",
    description="PyMT plugin for landlab",
    long_description=open("README.rst").read(),
    version=versioneer.get_version(),
    packages=packages,
    cmdclass=cmdclass,
    entry_points=entry_points,
    include_package_data=True,
)
