#    QASDAD, the quick and simple data analysis and documentation program
#    Copyright (C) 2018 Volker Weißmann . Contact: volker.weissmann@gmx.de

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

##If DEBUG is set to True, QASDAP will print
DEBUG=False
##If PROFILE is set to True, QASDAP will print the time for needed for various tasks
PROFILE=True

import time
#@cond INTERNAL
startTimeMillis = int(round(time.time() * 1000))
#@endcond INTERNAL
##Returns milliseconds since program startup
def millis():
	return int(round(time.time() * 1000))-startTimeMillis
if PROFILE:
	print("python.py started")

import sympy
from sympy import symbols
import sympy.physics
from sympy.physics.units import meter, second, hertz, kilogram, coulomb, volt, ampere, ohm, henry, kelvin, newton, joule, siemens, farad, watt
import numpy as np
import scipy.optimize
import math
import io #used in readFile
import os #used in Plot.showHere
#from enum import Enum
import matplotlib 
import matplotlib.pyplot #as plt
#import nfft
import latex2sympy

from .constants import *
from .units import *
from .table import *
from .equation import *
from .main import *
from .plot import *
from .calcColumn import *

if PROFILE:
	print(str(millis()) + " ms for importing")
