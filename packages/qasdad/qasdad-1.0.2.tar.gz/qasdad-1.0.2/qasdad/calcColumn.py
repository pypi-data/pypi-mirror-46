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

##Calculates a new Column from other Columns using a sympy equation
#Example usuage:
#col = calcColumn(table, "a + sin(b)", "c")
#this would calculate a Column col with the memName "c" and for every i the following equation would be true: col.data(i) = table["a"].data(i) + sin(table["b"].data(i))
#col.analPropUncert is a latex-string that holds the analytic propagation of uncertainty. Show with e.g. tex("$"+col.analPropUncert+"$")
#\param table: Accepts either a list, a dict or a table as an argument. (Note: The keys of the dictionary don't matter, the memName's do.)
#\param equation: The equation used to calculate the new column. Either a string, a sympy expression or an Equation is accepted.
#\param resultMemName: The memName of the calculated Column
#\param resultNameType: The nameType of the calculated Column
#\param resultMathName: The specialTexMathName of the calculated Column
#\param resultTextName: The specialTexTextName of the calculated Column
#\return: The calculated Column.
#Nice little Feature 1: If equation is an instance of Equation and resultMemName is None the memName of the calculated Column will be the left hand side of equation.
#Nice little Feature 2: If resultMathName is "equation" the specialTexMathName of the calculatedColumn is the latex representation of equation
#Nice little Feature 3: If resultTextName is "equation" the specialTexTextName of the calculatedColumn is the latex representation of equation
def calcColumn(table, equation, resultMemName=None, resultNameType="eq", resultMathName=None, resultTextName=None, examplePath=None):
	#TODO examplePath dokumentieren. Gucken ob das so die beste art und weise für das zurückgeben ist, oder ob calcColumn nicht besser eine Column und ein String zurückgeben sollte, o.ä.
	startTime = millis()
	if DEBUG:
		print("calcColumn called:")
		print("\ttable=", table)
		print("\tequation=", equation)
		print("\tresultMemName=", resultMemName)
		print("\tresultNameType=", resultNameType)
		print("\tresultMathName=", resultMathName)
		print("\tresultTextName=", resultTextName)
	willWeCalcExample = False
	if isinstance(equation, Equation):
		inverseDict = dict([[v,k] for k,v in equation.nameDict.items()])
		#(calcColumn(table, eq.eqSympy.rhs, str(eq.eqSympy.lhs), resultNameType="text", resultMathName=str(eq.eqSympy.lhs.subs(inverseDict)) ))
		resultMemName = str(equation.eqSympy.lhs)
		if resultMathName is None:
			resultMathName= str(equation.eqSympy.lhs.subs(inverseDict)) #TODO alternativ zu str(eq.eqSympy.lhs.subs(inverseDict)) könnte man doch auch den linken teil von eq.latex nehmen
		if resultTextName is None:
			resultTextName = "$" + resultMathName + "$"
		exampleEqLatex = equation.eqLatex
		equation = equation.eqSympy.rhs
		willWeCalcExample = True
	elif isinstance(equation, str):
		equation = strToSympy(equation)
	if resultMemName is None:
		print("bad argument for calcColumn: resultMemName is None")
		exit(1)
	if isinstance(table, Table):
		table = table.cols
	elif isinstance(table, dict):
		pass
	elif isinstance(table, list):
		table = {}
		for i in list:
			table[i.memName] = i
	else:
		print("bad argument for calcColumn: table has to of 'Table' or 'dict' or 'list' Type")
		exit(1)
	length = 1
	for a in table: #find length of all columns, store it in var length
		if length == 1 and len(table[a].rawData) != 1:
			length = len(table[a].rawData)
		elif length != len(table[a].rawData) and len(table[a].rawData) != 1:
			print("Fatal Error: Lengths don't match")
			exit(1)
	if resultMathName == "equation": #TODO das muss man dokumentieren, denn das weiß niemand von alleine
		resultMathName = sympy.latex(equation)
	if resultTextName == "equation": #TODO das muss man dokumentieren, denn das weiß niemand von alleine
		resultTextName = "$" + sympy.latex(equation) + "$"
	eqcp = equation
	for a in table:
		eqcp = eqcp.subs(table[a].memName, table[a].basicSIUnit)
	unit = checkGetUnit(eqcp)
	ret = Column(resultMemName, resultNameType, unit, [], specialTexMathName=resultMathName, specialTexTextName=resultTextName, rawDelta=[])
	exampleRow = length-1
	if willWeCalcExample:
		exampleCalc = "Beispielrechnung für die Berechnung von $" + ret.mathName() + "$ in Abhängigkeit von:\\begin{itemize}"
		for co in table:
			if sympy.symbols(table[co].memName) in equation.free_symbols:
				if len(table[co].rawData) == 1:
					i = 1
				else:
					i = exampleRow
				exampleCalc += "\\item $" + table[co].mathName() + "=" + ValueFormat(0,False).toNiceTexString(table[co].data(i),table[co].delta(i))  +"$"
		exampleCalc += "\\end{itemize}\\begin{equation}\\begin{aligned}" + exampleEqLatex + "\\\\="
		exampleStep = exampleEqLatex.split("=")[-1]
	for i in range(0,length): #Alle bekannten Werte einsetzen
		eqcp = equation
		for a in table:
			if len(table[a].rawData) != 1:
				val = table[a].data(i)
				delta = table[a].data(i)
			else:
				val = table[a].data(0)
				delta = table[a].data(0)
			eqcp = eqcp.subs(table[a].memName, val)
			if willWeCalcExample and i == exampleRow:
				exampleStep = exampleStep.replace(table[a].mathName(), ValueFormat(0,False).toNiceTexString(val,delta))
		try:
			val = eqcp.evalf()
			val = sympy.physics.units.convert_to(val, checkGetUnit(val))
			ret.rawData.append(val/unit)
		except:
			ret.rawData.append(-1)
			print("Fehler: Alle bekannten Größen wurden in die Gleichung eingesetzt, aber die Gleichung lässt sich trotzdem nicht zu einem float umformen. Die Gleichung ist:")
			print(equation)
			print(equation.args[0],type(equation.args[0]))
			print("und bekannte Größen sind:")
			for a in table:
				print(table[a].memName)
			print("Nach dem Einsetzen erhielten wir:")
			for a in table:
				equation = equation.subs(table[a].memName, table[a].data(i))
			print(equation.args)
			exit(1)
	#Ab hier sind alle Werte berechnet, alles ab hier ist fehlerrechnung
	#outfile = open(resultName+"_ff.tex","w")
	retFF = ""
	retFF += "\\begin{aligned}"
	retFF += "\\Delta " + ret.mathName()
	begin = True
	for co in table: #schreibt = delta x |df/dx| + delta y |df/dy| in die Datei
		if sympy.symbols(table[co].memName) in equation.free_symbols and not table[co].isDeltaZero():
			if begin:
				begin=False
				retFF += "="
			else:
				retFF += "+"
			retFF += "\\Delta " + table[co].mathName() + "\\left|\\frac{\\text d" + ret.mathName()  + "}{\\text d" + table[co].mathName() + "}\\right|"
	retFF += "\\\\"
	memNameMathNameDict = {} #zuordnung memName, mathName()
	for co in table:
		if sympy.symbols(table[co].memName) in equation.free_symbols:
			memNameMathNameDict[table[co].memName] =	table[co].mathName()
	diffDict = {} #symbolische Betragsableitungen
	for co in table: #diffDict berechen
		if sympy.symbols(table[co].memName) in equation.free_symbols and not table[co].isDeltaZero():
			diffDict[table[co].memName] = np.abs(sympy.diff(equation,sympy.symbols(table[co].memName)))
	begin = True
	for co in table: #schreibt = delta x |ableitung| + delta y |ableitung| in die Datei
		if sympy.symbols(table[co].memName) in equation.free_symbols and not table[co].isDeltaZero():
			if begin:
				begin=False
				retFF += "="
			else:
				retFF += "+"
			retFF += "\\Delta " + table[co].mathName() + sympy.latex(diffDict[table[co].memName].subs(memNameMathNameDict))
	retFF += "\\end{aligned}"
	#allNeededSymbols = [] #Liste aller symbole die es gibt aufstellen
	#for co in table:
	#	if sympy.symbols(table[co].memName) in equation.free_symbols:
	#		allNeededSymbols.append(table[co].memName)
	#vals = [] #Was wir für werte einsetzen werden
	#for sym in allNeededSymbols:
	#	vals.append(table[sym].data) #TODO Das macht probleme wenn table[c].memName  nicht memName ist
	#https://docs.sympy.org/latest/modules/numeric-computation.html
	#expr = sympy.symbols("ort")/sympy.symbols("zeit")
	#f = sympy.lambdify([sympy.symbols("ort"),sympy.symbols("zeit")], expr, "numpy")
	#o = np.array([1,2,3,4])
	#z = np.array([1,2,6,4])
	#t = [o,z]
	#print(f(*t))
	#exit(0)
	#diffLambdasDict = {} #alle Ableitungen als Lambdas schreiben
	#for d in diffDict:
	#	diffLambdasDict[d] = sympy.lambdify(allNeededSymbols, diffDict[d], "numpy")
	#diffNumDict = {}#alle Ableitungen mit zahlen eingesetzt
	#for d in diffDict:
	#	diffNumDict[d] = diffLambdasDict[d](vals) das funktioniert nicht wegen den Einheiten
	#print(diffNumDict)
	allSubs = [] #was allSubs ist findest du am besten mit print(allSubs) hinter dieser for-schleife heraus
	for i in range(0,length):
		allSubs.append({})
		for co in table:	
			if sympy.symbols(table[co].memName) in equation.free_symbols:
				if len(table[co].rawData) != 1:
					allSubs[i][table[co].memName] = table[co].data(i)
				else:
					allSubs[i][table[co].memName] = table[co].data(0)
	diffNumDict = {}
	for d in diffDict:
		diffNumDict[d] = []
		for i in range(0, length):
			diffNumDict[d].append(diffDict[d].subs(allSubs[i]).evalf())
	#ret.delta = []
	for i in range(0,length):
		delt = 0
		for m in diffDict:
			delt += table[m].delta(i)*diffNumDict[m][i] #TODO das macht probleme wenn table[m].memName != m ist
			#print(table[m].delta[i]*diffNumDict[m][i])
		ret.rawDelta.append(delt/unit)
	ret.analPropUncert = retFF
	if willWeCalcExample:
		exampleCalc += exampleStep + "\\\\=" + ValueFormat(0, False).toNiceTexString(ret.data(exampleRow), ret.data(exampleRow)) + "\\end{aligned}\\end{equation}"
	if examplePath is not None:
		file = open(examplePath, "w")
		file.write(exampleCalc)
		file.close()
	if PROFILE:
		print(str(millis()-startTime) + " ms for calcColumn")
	ret.rawData = np.array(ret.rawData)
	ret.rawDelta = np.array(ret.rawDelta) #TODO sobald der obrige teil umgeschrieben wird kann das hier weg
	return ret
def calcNfft(tCol,yCol,memName, memNamef): #TODO check wheter tCol has equal steps
	ft = np.fft.fft(yCol.rawData)[:len(yCol.rawData)//2]
	#ft = np.fft.fft(yCol.rawData)
	fty = Column(memName, "eq", tCol.basicSIUnit*yCol.basicSIUnit, np.abs(ft), rawDelta=None)
	ftx = Column(memNamef, "eq", 1/tCol.basicSIUnit, np.arange(0,len(ft))/np.array(tCol.rawData[-1]), rawDelta=None)
	return [fty, ftx]

