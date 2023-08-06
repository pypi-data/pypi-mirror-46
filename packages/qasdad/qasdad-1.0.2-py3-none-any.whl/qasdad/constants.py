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

from .qasdad import *

SPEED_OF_LIGHT = 299792458*meter/second
MAGNETIC_CONSTANT = 4*math.pi*10**-7*newton*ampere**-2
ELECTRIC_CONSTANT = 1/(4*math.pi*10**-7*newton*ampere**-2*299792458**2*meter**2*second**-2)
PLANCK_CONSTANT= 6.626070040*10**-34*joule*second
HBAR = 1.054571800*10**-34*joule*second
GRAVITATIONAL_CONSTANT = 6.67408*10**-11*meter**3*kilogram**-1*second**-2
ELEMENTARY_CHARGE = 1.6021766208*10**-19*coulomb
FINE_STRUCTURE_CONSTANT = 0.0072973525664

good_known_units_short = {
	"m": meter,
	"s": second,
	"Hz": hertz,
	"kg": kilogram,
	"C": coulomb,
	"V": volt,
	"A": ampere,
	"\Omega": ohm,
	"H": henry,
	"K": kelvin,
	"N": newton,
	"J": joule,
        "S": siemens,
        "W": watt
		    }
good_known_units_long = {
	"meter": meter,
	"second": second,
	"hertz": hertz,
	"kilogram": kilogram,
	"coulomb": coulomb,
	"volt": volt,
	"ampere": ampere,
	"ohm": ohm,
	"henry": henry,
	"kelvin": kelvin,
	"newton": newton,
	"joule": joule,
        "siemens": siemens,
        "watt": watt,
		    }
