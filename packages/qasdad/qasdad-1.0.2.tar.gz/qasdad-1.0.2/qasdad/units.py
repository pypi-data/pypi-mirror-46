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

#! [toBasicSI]
##\snippet this toBasicSI
def toBasicSI(unit):
	return sympy.physics.units.convert_to(unit,[sympy.physics.units.meter,sympy.physics.units.second,sympy.physics.units.kilogram,sympy.physics.units.coulomb,sympy.physics.units.kelvin])
#! [toBasicSI]
#! [subsSIUnitsOne]
##\snippet this subsSIUnitsOne
def subsSIUnitsOne(expr):
	expr = toBasicSI(expr)
	expr = expr.subs(sympy.physics.units.meter,1)
	expr = expr.subs(sympy.physics.units.second,1)
	expr = expr.subs(sympy.physics.units.kilogram,1)
	expr = expr.subs(sympy.physics.units.coulomb,1)
	expr = expr.subs(sympy.physics.units.kelvin,1)
	return expr
#! [subsSIUnitsOne]
##Exception that occurs if qasdad encounters incompatible dimensions, eg. 3*meter+5*second
class IncompDimensions(Exception):
	pass
##Exception that occurs if there is a free symbol in an expression that should not be there
class FreeSymbolException(Exception):
	pass
#@cond INTERNAL
def checkGetUnitBackend(a):
	try:
		float(a)
		return 1
	except:
		pass
        #TODO diese funktion dokumentiern und im source code nach sympy nach schauen welche isinstance befehler da noch fehlern
	if isinstance(a,sympy.add.Add):
		u = checkGetUnitBackend(a.args[0])
		for i in range(1,len(a.args)):
			#print(a.args[i])
			#print(unit(toBasicSI(u))) meter
			#print(checkGetUnit(toBasicSI(u))) meter
			#print(toBasicSI(checkGetUnitBackend(a.args[i])))
			#if unit(toBasicSI(checkGetUnitBackend(a.args[i]))) != unit(toBasicSI(u)):
			if checkGetUnitBackend(toBasicSI(a.args[i])) != checkGetUnitBackend(toBasicSI(u)):
				print("=============================")
				print(toBasicSI(checkGetUnitBackend(a.args[i])))
				print(toBasicSI(u))
				raise IncompDimensions("incompatible dimensionen")
		return u
	elif isinstance(a,sympy.mul.Mul):
		u = 1
		for arg in a.args:
			u *= checkGetUnitBackend(arg)
		return u
	elif isinstance(a, sympy.power.Pow):
		return checkGetUnitBackend(a.args[0])**a.args[1]
	elif (isinstance(a, sympy.sin) or isinstance(a, sympy.asin) or
	      isinstance(a, sympy.cos) or isinstance(a, sympy.acos) or
	      isinstance(a, sympy.tan) or isinstance(a, sympy.atan)):
		if checkGetUnitBackend(a.args[0]) != 1:
			print("incompatible dimension: The following is not dimensionless but should be")
			print(a.args[0])
			exit(1)
		return 1
	elif isinstance(a, sympy.log):
		for arg in a.args:
			checkGetUnitBackend(arg)
		return 1
	elif isinstance(a, sympy.physics.units.quantities.Quantity):
		return a
	elif isinstance(a, sympy.symbol.Symbol):
		raise FreeSymbolException(str(a))
	else:
		raise IncompDimensions("unsup. op")
		print("unsupported operation for checkGetUnitBackend", type(a))
		exit(1)
#@endcond INTERNAL
##Returns the unit of expr. Exits with errorcode 1 if it encounters incompatible dimensions, eg. 3*meter+5*second
def checkGetUnit(expr):
	#print("============================")
	if DEBUG:
		print("\tcheckGetUnit:")
		print("\t\t", expr)
	try:
		u = checkGetUnitBackend(expr)
	except FreeSymbolException as ex:
		print("Fatal Error: Unable to check and get unit of: ")
		print(expr)
		print("Because of the free symbol:")
		print(ex)
		exit(1)
	if DEBUG:
		print("\t\treturns:", u)
	return u
#@cond INTERNAL
def checkGetUnitTest():
	print("testing checkGetUnit...")
	goodPairs = [[7.4*sympy.physics.units.meter, sympy.physics.units.meter],
		     [1.0*sympy.physics.units.meter, sympy.physics.units.meter],
		     [1*sympy.physics.units.meter, sympy.physics.units.meter],
		     [5*sympy.physics.units.meter, sympy.physics.units.meter],
		     [sympy.physics.units.meter, sympy.physics.units.meter],
		     [3*sympy.physics.units.centimeter + sympy.physics.units.meter, sympy.physics.units.meter, sympy.physics.units.centimeter]]
	
	for pair in goodPairs:
		flag = False
		u = checkGetUnit(pair[0])
		for i in range(1, len(pair)):
			if u == pair[i]:
				flag = True
		assert(flag)
	print("...finished testing checkGetUnit")
if DEBUG:
	checkGetUnitTest()
#@endcond INTERNAL
