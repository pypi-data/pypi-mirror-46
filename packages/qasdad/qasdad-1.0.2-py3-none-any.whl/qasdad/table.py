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

##Column is intended to hold a physical property that has different values in different repititions of the same experiment
class Column:
	##The name that is used to address this Column within this Program (mem is short for memory)
	memName = None
	##Unit of the physical property. subsSIUnitsOne(basicSIUnit) has to return 1
	basicSIUnit = None
	##rawData is a numpy array hat holds the value of the physical property (without a unit) rawData*basicSIUnit is the value of the physical property
	rawData = None
	##rawDelta is  a numpy array that holds the measuring inaccuracy (without a unit) rawDelta*basicSIUnit is the measuring inaccuracy
	#delta may be None
	#If rawDelta is not None the lengths of rawData and rawDelta have to be equivalent
	rawDelta = None
	##Read the documention of mathName
	specialTexMathName = None
	##Read the documention of textName
	specialTexTextName = None
	##Read The documention of mathName and textName
	nameType = None
	##analPropUncert sometimes holds a latex-formatted string of a analytic propagation of uncertainty. Show with tex("$"+col.analPropUncert+"$")
	analPropUncert = None
	#! [Column mathName]
	##\snippet this Column mathName
	##\return Symbol of the physical property that should be used in equations
	def mathName(self):
		if self.specialTexMathName is not None:
			return self.specialTexMathName
		if self.nameType == "eq":
			return self.memName
		if self.nameType == "text":
			return "\\mathrm{" + self.memName + "}"
		print("malformed Column")
		exit(1)
	#! [Column mathName]
	#! [Column textName]
	##\snippet this Column textName
	##\return Name of the physical property that should be used in text
	def textName(self):
		if self.specialTexTextName is not None:
			return self.specialTexTextName
		if self.nameType == "text":
			return self.memName
		if self.nameType == "eq":
			return "$" + self.memName + "$"
		print("malformed Column")
		exit(1)
	#! [Column textName]
	#! [Column data]
	##\snippet this Column data
	##\return Value of the physical property including its unit
	def data(self, index):
		return self.rawData[index]*self.basicSIUnit
	#! [Column data]
        #! [Column delta]
        ##\snippet this Column delta
	##\return Uncertainty of the physical property including its unit
	def delta(self, index):
		return self.rawDelta[index]*self.basicSIUnit
	#! [Column delta]
	##\return Returns True if the physical property is exact
	def isDeltaZero(self):
		if DEBUG:
			print("\tisDeltaZero:")
			print("\t\tself.memName=", self.memName)
		if self.rawDelta is None:
			if DEBUG:
				print("\t\treturn True")
			return True
		for i in self.rawDelta:
			if i != 0:
				if DEBUG:
					print("\t\treturn False")
				return False
		if DEBUG:
			print("\t\treturn True")
		return True
	#Constructor:
	#\param memName The name that is used to address this Column within this Program (mem is short for memory).
	#\param nameType Look at the documentation of Column.mathName and Column.textName for explanation.
	#\param basicSIUnit Unit of the physical property. subsSIUnitsOne(basicSIUnit) has to return 1
	#\param rawData The value of the physical property without its unit. The data type of rawData has to be "list".
	#\param rawDelta The uncertainty of the physical property without its unit. The data type of rawDelta has to be "list".
	##Constructor: Checks if data is an instance of the "list"-class and sets member variables according to arguments
	def __init__(self, memName, nameType, basicSIUnit, rawData, specialTexMathName=None, specialTexTextName=None, rawDelta=None):#TODO nameType soll ein optionales argument sein, wenn texMathName und texTextName gegeben sind
		if subsSIUnitsOne(basicSIUnit) != 1:
			raise ValueError("subsSIUnitsOne(basicSIUnit) != 1")
		#if not isinstance(rawData, np.ndarray):
		#	raise ValueError("rawData should be a numpy ndarray but is of type: ", type(rawData))
		#if rawDelta is not None and not isinstance(rawDelta, np.ndarray):
		#	raise ValueError("rawDelta should be None or a numpy ndarray but is of type: ", type(rawDelta))
		#TODO check if rawData and rawDelta are numpy arrays
		self.memName = memName
		self.nameType = nameType
		self.basicSIUnit = basicSIUnit
		self.rawData = rawData
		self.specialTexMathName = specialTexMathName
		self.specialTexTextName = specialTexTextName
		self.rawDelta = rawDelta
	##Only Used for debug purposes, exact format is not guaranteed to be stable
	def __str__(self):
		ret = "<" + self.memName
		for i  in self.data:
			ret += " " + str(i) #self.format.format(i)
		ret += ">"
		return ret
	##Only Used for debug purposes, exact format is not guaranteed to be stable
	def __repr__(self):
		return str(self)

##Table is a super thin wrapper around python's dict that ensures that self.cols[key].memName == key
class Table:
        #! [table init]
	##\snippet this table init
	def __init__(self, copy=None):
		if copy is None:
			self.cols = {}
		elif isinstance(copy, Table):
			self.cols = copy.cols #shallow copy
			#print("=====================")
			#print(copy.cols)
			#self = copy #TODO #pythonlernen wieso geht das nicht
			#print(self.cols)
			#print("=====================")
		elif isinstance(copy, list):
			self.cols = {} #shallow copy
			for i in copy:
				self.cols[i.memName] = i
		elif isinstance(copy, dict):
			self.cols = copy #shallow copy
		else:
			print("bad arguments for Table.init")
			exit(1) #TODO raise wäre besser
	#! [table init]
	#! [table getitem]
	##\snippet this table getitem
	def __getitem__(self, key):
		return self.cols[key]
	#! [table getitem]
	#! [table setitem]
	##\snippet this table setitem
	def __setitem__(self, key, value):
		if value.memName != key:
			print("key and memName do not match")
			exit(1)
		self.cols[key] = value
	#! [table setitem]
	#! [table add]
	##\snippet this table add
	def add(self, value):#TODO: should we call this method "add" or "set"?
		if isinstance(value, Column):
			self.cols[value.memName] = value
			return
		elif isinstance(value, Table):
			value = list(value.cols.values())
		elif isinstance(value, dict):
			value = list(value.values())
		elif isinstance(value, list):
			pass
		else:
			print("Bad argument type for Table.add")
			exit(1)#TODO: raise would be better than exit, is there a "wrongTypeException" in python?
		for c in value:
			self.cols[c.memName] = c
	#! [table add]
	##\deprecated
	def addFromEq(self, eq):
		print("use of deprecated function add Table.addFromEq, use calcColumn instead")
		exit(1)
		#print(eq.eqSympy)
		#print(str(eq.eqSympy.lhs))
		#if str(eq.eqSympy.lhs) in eq.nameDict:
		#	memName = eq.nameDict[str(eq.eqSympy.lhs)]
		#else:
		#	memName = str(eq.eqSympy.lhs)
		inverseDict = dict([[v,k] for k,v in eq.nameDict.items()])
		self.add(calcColumn(table, eq.eqSympy.rhs, str(eq.eqSympy.lhs), resultNameType="text", resultMathName=str(eq.eqSympy.lhs.subs(inverseDict)) ))
	def checkGetLen(self):#TODO diese Funktion dokumentieren
		length = 1
		for mem in self.cols:
			if length == 1:
				length = len(self.cols[mem].data)
			elif length != len(self.cols[mem].data):
				print("Error in checkGetLen") #TODO raise wäre besser
				exit(1)
		return length
	def removeRows(self, condition): #TODO: Document this function #TODO mit map kann man das besser schreiben
		condition = strToSympy(condition)
		rowNum = 0
		while rowNum < self.checkGetLen():
			cond = condition
			for mem in self.cols:
				cond = cond.subs(mem, self.cols[mem].data[rowNum])
			if cond:
				for mem in self.cols:
					del self.cols[mem].data[rowNum]
					#self.cols[mem].data = np.delete(self.cols[mem].data, rowNum)
			else:
				rowNum += 1
			
