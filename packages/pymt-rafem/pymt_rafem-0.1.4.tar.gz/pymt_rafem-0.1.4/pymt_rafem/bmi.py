from __future__ import absolute_import

import os

import pkg_resources
from rafem import BmiRiverModule as Rafem

Rafem.__name__ = "Rafem"
Rafem.METADATA = os.path.abspath(
    pkg_resources.resource_filename("pymt_rafem", "data/Rafem")
)
