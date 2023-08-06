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

__all__ = [
    "OverlandFlow",
    "Flexure",
    "LinearDiffuser",
    "ExponentialWeatherer",
    "TransportLengthHillslopeDiffuser",
    "Vegetation",
    "SoilMoisture",
    "DepthDependentDiffuser",
]
