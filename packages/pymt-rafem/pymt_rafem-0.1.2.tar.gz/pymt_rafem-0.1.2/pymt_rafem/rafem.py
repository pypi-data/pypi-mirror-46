from __future__ import absolute_import

from pymt.framework.bmi_bridge import bmi_factory
from rafem import BmiRiverModule


Rafem = bmi_factory(BmiRiverModule)
