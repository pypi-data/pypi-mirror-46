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

TEX_FILE = None
def setTexFile(texfile):
	global TEX_FILE
	TEX_FILE = texfile

#! [tex]
##\snippet this tex
def tex(*args):
	for a in args:
		TEX_FILE.write(str(a)) #_TEX_FILE_ gets set by the qasdad executer.
#! [tex]
##Prints every part of a sympy expression. Only for debug purposes
def debugPrintExprArgs(expr):
	if len(expr.args) == 0:
		print(expr)
	else:
		for a in expr.args:
			debugPrintExprArgs(a)
##Convert a string to a sympy expression. Supports equal signs every unit from good_known_units_long
def strToSympy(expr):
	#expr = sympy.parsing.sympy_parser.parse_expr(expr)
	expr = sympy.parsing.sympy_parser.parse_expr(expr, evaluate=False, transformations=(sympy.parsing.sympy_parser.standard_transformations + (sympy.parsing.sympy_parser.convert_equals_signs,)))
	expr = expr.subs(sympy.sqrt(-1), sympy.symbols("I"))
	expr = sympy.simplify(expr)
	#expr = sympy.sympify(expr)
	for u in good_known_units_long:
		expr = expr.subs(symbols(u), good_known_units_long[u])
	return expr
##Simpliflies an expression. E.g simplify(5*joule + 7*newton*meter) = 12*joule
def simplify(expr):
	print(expr)
##Check if table contains columns with len(data) == 1. If so, substitute the memName of the column with data[0] in expr
##\param expr: Accepts either a sympy expression or an instance of Equation as an argument.
##\param table: Accepts either a list, a dict or a table as an argument. (Note: The keys of the dictionary don't matter, the memName's do.)
def subsOneValColumn(expr, table):
	if isinstance(table, Table):
		table = list(table.cols.values())
	elif isinstance(table, dict):
		table = list(table.values())
	elif isinstance(table, list):
		pass
	else:
		print("bad argument for subsOneValColumn: table is not of 'Table' or 'dict' or 'list' Type")
		exit(1)
	if isinstance(expr, Equation):
		for c in table:
			if len(c.data) == 1:
				expr.eqSympy = expr.eqSympy.subs(c.memName, c.data[0])
	else:
		for c in table:
			if len(c.data) == 1:
				expr = expr.subs(c.memName, c.data[0])
	return expr
##Returns expr without the its. Note that it does not care whether the unit is a basic SI unit or not, use subsSIUnitsOne instead if you want to compare values. Note: It's probably super buggy and will (hopefully) be rewritten soon.
def withoutUnit(expr): #source: https://stackoverflow.com/questions/51119918/how-to-concisely-get-the-units-of-a-sympy-expression?rq=1
	try:
		float(expr)
		return expr
	except:
		pass
	#if isinstance(expr.evalf(), sympy.numbers.Float):
	#	return expr
	expr = 1.0*expr
	return float(expr.subs({x: 1 for x in expr.args if x.has(sympy.physics.units.Quantity)}))
##converts units and sympy expressions to nice formattet latex code. For Numbers use niceNumberPrintDigits and niceNumberPrintDelta instead
def anythingExceptNumbersToTex(expr):#https://stackoverflow.com/questions/23824687/text-does-not-work-in-a-matplotlib-label
	if isinstance(expr, str):
		expr = strToSympy(expr)
	#unit = sympy.latex(unit).replace(" ", "cdot ")
	expr = sympy.latex(expr).replace("\\text", "\\mathrm")
	for u in good_known_units_short:
		expr = expr.replace(str(good_known_units_short[u]), "\\mathrm{" + u + "}")
	return expr
##Converts a value to a nicely formatted latex string
##\param digits: number of significant of digits
##\return Nicely formatted latex string e.g. 1,245\cdot 10^4 \\mathrm{m}
def niceNumberPrintDigits(value, digits):
	if isinstance(value, float):
		numValue = value
	else:
		numValue = withoutUnit(value)
	if numValue != 0:
		expValue = math.floor(math.log(abs(numValue), 10))
	else:
		expValue = 0
	ret = ""
	#ret += ("{:." + str(digits) +  "n}").format(numValue/10**expValue)
	ret += ( ("%." + str(digits) + "f") % (numValue/10**expValue) ).replace(".", ",")
	ret += "\cdot 10^{" + str(expValue) + "}"
	#if not isinstance(value,float):
	if checkGetUnit(value) != 1:
		ret += "\," + anythingExceptNumbersToTex(checkGetUnit(value))
	return ret
##Converts a value to a nicely formatted latex string
##\param delta: measurement uncertainty
##\return Nicely formatted latex string e.g. 1,245(1)\\cdot 10^4 \\mathrm{m}
def niceNumberPrintDelta(value, delta):
	if isinstance(value, float):
		numValue = value
		numDelta = delta
	else:
		numValue = withoutUnit(value)
		numDelta = withoutUnit(delta)
	if numValue != 0:
		expValue = math.floor(math.log(abs(numValue), 10))
	else:
		expValue = math.floor(math.log(abs(numDelta), 10))
	digits = expValue-math.floor(math.log(numDelta, 10))+1
	ret = ""
	#ret += ("{:." + str(digits) +  "n}").format(numValue/10**expValue)
	ret += ( ("%." + str(digits) + "f") % (numValue/10**expValue) ).replace(".", ",")
	ret += "(" + str(math.ceil(numDelta*10**(digits-expValue-1)))  + ")"
	ret += "\cdot 10^{" + str(expValue) + "}"
	#if not isinstance(value,float):
	if checkGetUnit(value) != 1:
		ret += "\," + anythingExceptNumbersToTex(checkGetUnit(value))
	return ret
def isnan(expr): #TODO diese Funktion dokumentieren
	if isinstance(expr, float):
		return math.isnan(expr)
	else:
		return expr == sympy.nan
	#if isinstance(expr, ):
	#	return math.isnan(expr)
##NumberFormat is a class that holds a specific way to print a value, eg Scientific Notation with 4 valid Digits and no uncertainty
class ValueFormat: #Why the f#@* does python not have real rust-like enums?
	##numDigits stores the number of valid digits that will be printed. If numDigits is 0 the number of digits that will be printed is inferred by the uncertainty of that value
	numDigits = 0
	##showDelta stores whether the uncertainty should be printed?
	showDelta = True
	#! [ValueFormat init]
	##\snippet this ValueFormat init
	def __init__(self, numDigits, showDelta):
		self.numDigits = numDigits
		self.showDelta = showDelta
	#! [ValueFormat init]
	##Returns the value "value" as a nice latex string. Acts if showDelta is False if delta is NaN. Crashes if value is NaN.
	def toNiceTexString(self, value, delta=None):
		ar = self.toNiceTexList(value, delta)
		ret = ""
		for s in ar:
			ret += s
		return ret
	##Length of the list returned by toNiceTexList
	listLength = 3 #TODO is it possible in python to declare this as static or constant
	##Similar to toNiceTexString, but splits the result into a list of the length "ValueFormat.listLength". E.g. ValueFormat(0,True).toNiceTexList(213,2) = ['2,130(2)', '\\cdot 10^{2}']
	def toNiceTexList(self, value, delta=None):
		ret = ["", "", ""]
		if delta is None and (self.showDelta == True or self.numDigits == 0):
			print("Bad arguments for toNiceTexList")
			exit(1)
		if isinstance(value, float):
			numValue = value
			numDelta = delta
		else:
			numValue = withoutUnit(value)
			numDelta = withoutUnit(delta) #PERFORMANCE: If numDigits is not 0 and showDelta is False
		if numValue != 0:
			expValue = math.floor(math.log(abs(numValue), 10))
		elif not isnan(delta):
			expValue = math.floor(math.log(abs(numDelta), 10))
		else:
			expValue = 1
		digits = self.numDigits
		if digits == 0:
			if not isnan(delta):
				digits = expValue-math.floor(math.log(numDelta, 10))+1
				digits = max(0,digits) #If value << delta, digits would get negative and formatting would fail
			else:
				digits = 3
		if numValue < 0:
			ret[0] = "-"
		ret[1] = ( ("%." + str(digits) + "f") % (abs(numValue)/10**expValue) ).replace(".", "{,}")
		if self.showDelta and not isnan(delta):
			ret[1] += "(" + str(math.ceil(numDelta*10**(digits-expValue-1)))  + ")"
		if expValue != 0:
			ret[2] += "\cdot 10^{" + str(expValue) + "}"
		if checkGetUnit(value) != 1:
			ret[2] += "\," + anythingExceptNumbersToTex(checkGetUnit(value))
		return ret
                
##Reads a file and returns a table
#File Format: e.g.\n
#\#t ;vx_1 ;vx_2\n
#\#s ; 0.0254*m ; 10**3*m\n
#10,35 1.00 0.796\n
#35.10 900 4,3\n
#The first line contains the memNames of the Coloumns: time, x_1 and x_2\n
#The "text" and "eq" specify whether the memName should be printed in a latex-text environment or a latex-math environment. For more information take a look at Column.mathName and Column.textName\n
#The second line gets multiplied with every line. This is useful for declaring units and 10^n's. For a total list of supported units look at good_known_units_short. SI unit prefixes are not supported. In this example, the first column would be in seconds, the second column in inch and the third column in kilometers.\n
#In the first two lines whitespaces get ignored if they are not within a memName\n
#From the third line onwards, both "," and "." have the same meaning, the decimal seperator.\n
#If this description of the file seems ambigious for you, take a look at the source code of this function.\n
#Security notice: readFile uses sympy.sympyfy which uses eval() which should not be used on untrusted input. Therefore, readFile(filepath) should only be run if filepath is at least as trustworthy as this script.
def readFile(filepath, memNames=None, unitFactor=None): #TODO Dokument the memNames and unitFactor argument
	if PROFILE:
		startTime = millis()
	with open(filepath) as fp:
		if memNames is None:
			memNames = fp.readline().split(";")
			memNames[0] = memNames[0][1:]
			memNames = [o.lstrip().rstrip() for o in memNames]
			for i in range(0, len(memNames)): #TODO is there a more pythonic way to do that
				if memNames[i].startswith("eq:"):
					memNames[i] = memNames[i][3:]
			memNames = [o.lstrip().rstrip() for o in memNames]
		if unitFactor is None:
			unitFactor = fp.readline().split(";")
			unitFactor[0] = units[0][1:]
		units = [sympy.sympify(o).subs(good_known_units_short) for o in unitFactor]
		factors = [subsSIUnitsOne(u) for u in units]
		for i in range(0, len(units)): #TODO is there a more pythonic way to do that
			units[i] = units[i]/factors[i]
		factors = [float(f) for f in factors]
		ret = Table()
		filestr = ""
		with open(filepath) as fp:  
			for line in fp:
				filestr += line.replace(";", "\t").replace(",", ".")
		if PROFILE:
			startTime2 = millis()
		matrix = np.loadtxt(io.StringIO(filestr), dtype=str)
		if PROFILE:
			print(str(millis()-startTime2) + " ms for np.loadtxt")
		if len(matrix[0]) != len(memNames):
			print("The length of memNames does not match the num of Columns in the file")
			raise ValueError
		if len(matrix[0]) != len(unitFactor):
			print("The length of unitFactor does not match the num of Columns in the file")
			raise ValueError
		for i in range(0,len(matrix[0])):
			dat = [float(o) for o in matrix[:,i]]
			rawDelta = []
			for o in matrix[:,i]:
				ar = o.split(".")
				digits = 0
				if len(ar) == 2:
					digits = len(ar[1])
				rawDelta.append(10**(-digits))
			dat = np.array(dat)*factors[i]
			rawDelta = np.array(rawDelta)*factors[i]
			ret.add(Column(memNames[i],"eq",units[i],dat,rawDelta=rawDelta))
	if PROFILE:
		print(str(millis()-startTime) + " ms for readFile including np.loadtxt")
	return ret
##Prints table. Only for debug purposes Note: This function likes to crash.
def debugTableRaw(table):
	if not isinstance(table, Table):
		print("bad arguments for debugTableRaw: table is not an instance of class Table")
		exit(1)
	ret = "#"
	for a in table.cols:
		if table[a].memName != "_num":
			table[a].maxDataSpace = len(table[a].memName)
			table[a].maxDeltaSpace = 0
			for i in table[a].data:
				if len(str(i)) > table[a].maxDataSpace:
					table[a].maxDataSpace = len(str(i))
			if table[a].delta is not None:
				for i in table[a].delta:
					if len(str(i)) > table[a].maxDeltaSpace:
						table[a].maxDeltaSpace = len(str(i))
			ret += table[a].memName + " "*(1+table[a].maxDataSpace-len(table[a].memName) )
	#for i in self.data[0].data: das würde zu bugs nach führen wenn erst sort(), dann str() aufgerufen wird
	#len(table[0].data)
	maxLength = 0
	for a in table.cols:
		if len(table[a].data) > maxLength:
			maxLength = len(table[a].data)
	for i in range(0,maxLength): #TODO was wenn nicht alle Tabellen gleich lang sind
		ret += "\n "
		for a in table.cols:
#			if table[a].memName != "_num":
			#ret += str(a.data[i]) + " "*(1+a.maxDataSpace-len(str(a.data[i])) )
			if len(table[a].data) > i:
				msg = str(table[a].data[i])
			else:
				msg = "leer"
			ret += msg + " "*(1+table[a].maxDataSpace-len(msg) ) #+ "+- " +  str(table[a].delta[i]) + " "
			if table[a].delta is not None and len(table[a].delta) > i:
				msg = str(table[a].delta[i])
			else:
				msg = "leer"
			ret += "+- " + msg + " "*(1+table[a].maxDeltaSpace-len(msg) )
	print(ret)
##Prints table. Only for debug purposes Note: This function likes to crash.
def debugTableNice(table): #TODO: print(table) should execute this funktion
	if not isinstance(table, Table):
		print("bad arguments for debugTableNice: table is not an instance of class Table")
		exit(1)
	ret = "#"
	for a in table.cols:
		if table[a].memName != "_num":
			table[a].maxSpace = len(table[a].memName)
			for i in range(0,len(table[a].data)):
				length = len(niceNumberPrintDelta(table[a].data[i],table[a].delta[i]))
				if length > table[a].maxSpace:
					table[a].maxSpace = length
			ret += table[a].memName + " "*(1+table[a].maxSpace-len(table[a].memName) )
	#for i in self.data[0].data: das würde zu bugs nach führen wenn erst sort(), dann str() aufgerufen wird
	#len(table[0].data)
	maxLength = 0
	for a in table.cols:
		if len(table[a].data) > maxLength:
			maxLength = len(table[a].data)
	for i in range(0,maxLength): #TODO was wenn nicht alle Tabellen gleich lang sind
		ret += "\n "
		for a in table.cols:
#			if table[a].memName != "_num":
			#ret += str(a.data[i]) + " "*(1+a.maxSpace-len(str(a.data[i])) )
			if len(table[a].data) > i:
				msg = niceNumberPrintDelta(table[a].data[i],table[a].delta[i])
			else:
				msg = "leer"
			ret += msg + " "*(1+table[a].maxSpace-len(msg) ) #+ "+- " +  str(table[a].delta[i]) + " "
	print(ret)
##Uses the tex(...) command to show table as a a nicely formatted latex tabular
#\param table: Accepts either a list, a dict or a table as an argument. (Note: The keys of the dictionary don't matter, the memName's do.)
#\param format: Decides how the values should be printed. This argument should be a list of ValueFormat instances
#\param path: Writes the tabular into a file with the filepath "path"
def showAsTabular(table, format=None, path=None):
	if PROFILE:
		startTime = millis()
	if isinstance(table, Table):
		table = list(table.cols.values())
	elif isinstance(table, dict):
		table = list(table.values())
	elif isinstance(table, list):
		pass
	else:
		print("Bad argument for showAsTabular: table is not of 'Table' or 'dict' or 'list' Type")
		exit(1)
	if format is not None and not isinstance(format, dict):
		print("Bad argument for showAsTabular: format is neither None nor a 'dict'")
		exit(1)
	if path is not None:
		texfile = open(path, 'w')
	else:
		texfile = TEX_FILE
	texfile.write("\\begin{tabular}{" + (("l"*ValueFormat.listLength)+"|")*(len(table)-1) + "l"*ValueFormat.listLength + "}\n") #"r|"*(len(table)*ValueFormat.listLength-1)
	begin = True
	for c in table:
		if begin:
			begin = False
			texfile.write("\\multicolumn{" + str(ValueFormat.listLength) + "}{c}{")
		else:
			texfile.write("&\\multicolumn{" + str(ValueFormat.listLength) + "}{|c}{")
		texfile.write("$" + c.mathName() + "$") #TODO: Dokumentation anpassen
		if c.basicSIUnit != 1:
			texfile.write(" [$" + anythingExceptNumbersToTex(c.basicSIUnit)  + "$]")
		texfile.write("}")
		#texfile.write("&"*(ValueFormat.listLength-1))
	texfile.write("\\\\\\hline\n")
	maxLength = 0
	for c in table:
		if len(c.rawData) > maxLength:
			maxLength = len(c.rawData)
	for i in range(0,maxLength):
		begin = True
		for c in range(0,len(table)):
			if begin:
				begin = False
			else:
				texfile.write("&")
			if len(table[c].rawData) > i:
				if format is not None and table[c].memName in format:
					fmt = format[table[c].memName]
				else:
					fmt = ValueFormat(0,False)
				if math.isnan(table[c].rawData[i]):
					for i2 in range(1,ValueFormat.listLength):
						texfile.write("&\\hspace{-1em}")
				else:
					ar = fmt.toNiceTexList(table[c].rawData[i], table[c].rawDelta[i])
					texfile.write("$" + ar[0] + "$")
					for i2 in range(1,len(ar)):
						texfile.write("&\\hspace{-1em}$" + ar[i2] + "$")
				#texfile.write("$" + fmt.toNiceTexString(withoutUnit(table[c].data[i]), withoutUnit(table[c].delta[i])) + "$")
				#texfile.write("$" + niceNumberPrintDelta( withoutUnit(c.data[i]), withoutUnit(c.delta[i]) ) + "$")
			else:
				texfile.write("&"*(ValueFormat.listLength-1))
		texfile.write("\\\\\n")
	texfile.write("\\end{tabular}\\\\")
	if path is not None:
		texfile.close()
	if PROFILE:
		print(str(millis()-startTime) + " ms for showAsTabular")
#! [showAsTable]
##\snippet this showAsTable
def showAsTable(table, label, caption, format=None):
	tex("\\begin{table}[H]")
	showAsTabular(table, format)
	tex("\\caption{" + caption + "}")
	tex("\\label{" + label + "}")
	tex("\\end{table}")
#! [showAsTable]
def getMaxima(col): #TODO document this function
	x = []
	y = []
	for i in range(1, len(col.rawData)-1):
		if col.rawData[i] > col.rawData[i-1] and col.rawData[i] > col.rawData[i+1]:
			x.append(i)
			y.append(col.rawData[i])
	return x,y
def testGetMaxima(path, x, y): #TODO document this function
	table = readFile(path)
	p = Plot(display=True)
	p.add("", table[x], table[y], xerr=False, yerr=False)
	a,b = getMaxima(table[y])
	for i in range(0, len(a)):
		a[i] = table[x].rawData[a[i]]
	p.ax.plot(a, b, linestyle="", marker="+")
	#p.showHere()
	matplotlib.pyplot.show()
