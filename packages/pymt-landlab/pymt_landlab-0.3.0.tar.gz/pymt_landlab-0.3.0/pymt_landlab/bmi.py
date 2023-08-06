from __future__ import absolute_import
import os
import pkg_resources


from landlab.bmi.components import OverlandFlow as OverlandFlow
from landlab.bmi.components import Flexure as Flexure
from landlab.bmi.components import LinearDiffuser as LinearDiffuser
from landlab.bmi.components import ExponentialWeatherer as ExponentialWeatherer
from landlab.bmi.components import TransportLengthHillslopeDiffuser as TransportLengthHillslopeDiffuser
from landlab.bmi.components import Vegetation as Vegetation
from landlab.bmi.components import SoilMoisture as SoilMoisture
from landlab.bmi.components import DepthDependentDiffuser as DepthDependentDiffuser
from landlab.bmi.components import FlowDirectorSteepest as FlowDirectorSteepest
from landlab.bmi.components import FlowAccumulator as FlowAccumulator
from landlab.bmi.components import StreamPowerEroder as StreamPowerEroder
from landlab.bmi.components import FlowRouter as FlowRouter
from landlab.bmi.components import FlowDirectorD8 as FlowDirectorD8
from landlab.bmi.components import FlowDirectorDINF as FlowDirectorDINF


OverlandFlow.__name__ = "OverlandFlow"
OverlandFlow.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/OverlandFlow")
)

Flexure.__name__ = "Flexure"
Flexure.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/Flexure")
)

LinearDiffuser.__name__ = "LinearDiffuser"
LinearDiffuser.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/LinearDiffuser")
)

ExponentialWeatherer.__name__ = "ExponentialWeatherer"
ExponentialWeatherer.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/ExponentialWeatherer")
)

TransportLengthHillslopeDiffuser.__name__ = "TransportLengthHillslopeDiffuser"
TransportLengthHillslopeDiffuser.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/TransportLengthHillslopeDiffuser")
)

Vegetation.__name__ = "Vegetation"
Vegetation.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/Vegetation")
)

SoilMoisture.__name__ = "SoilMoisture"
SoilMoisture.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/SoilMoisture")
)

DepthDependentDiffuser.__name__ = "DepthDependentDiffuser"
DepthDependentDiffuser.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/DepthDependentDiffuser")
)

FlowDirectorSteepest.__name__ = "FlowDirectorSteepest"
FlowDirectorSteepest.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/FlowDirectorSteepest")
)

FlowAccumulator.__name__ = "FlowAccumulator"
FlowAccumulator.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/FlowAccumulator")
)

StreamPowerEroder.__name__ = "StreamPowerEroder"
StreamPowerEroder.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/StreamPowerEroder")
)

FlowRouter.__name__ = "FlowRouter"
FlowRouter.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/FlowRouter")
)

FlowDirectorD8.__name__ = "FlowDirectorD8"
FlowDirectorD8.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/FlowDirectorD8")
)

FlowDirectorDINF.__name__ = "FlowDirectorDINF"
FlowDirectorDINF.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_landlab", "data/FlowDirectorDINF")
)

__all__ = [
    "OverlandFlow",
    "Flexure",
    "LinearDiffuser",
    "ExponentialWeatherer",
    "TransportLengthHillslopeDiffuser",
    "Vegetation",
    "SoilMoisture",
    "DepthDependentDiffuser",
    "FlowDirectorSteepest",
    "FlowAccumulator",
    "StreamPowerEroder",
    "FlowRouter",
    "FlowDirectorD8",
    "FlowDirectorDINF",
]
