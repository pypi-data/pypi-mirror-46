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

##Holds an equation, consisting of a sympy equation, a latex equation and a dictionary that matches latex representations to sympy symbols
class Equation:
	##equation as a sympy equation
	#Note: You can get the left side of the equation via object.eqSympy.lhs and the right side similar.
	eqSympy = None
	##equation as a latex string
	eqLatex = None
	##dictionary that matches latex representations to sympy symbols.
	#Note: {latexString: sympySymbol} not {sympySymbol: latexString}
	nameDict = None
	##Construct an Equation from a sympy equation and a dictionary that matches latex representations to sympy symbols. Note: THIS IS CURRENTLY BROKEN
	@staticmethod
	def fromSympy(expr, nameDict):
		if PROFILE:
			startTime = millis()
		if isinstance(expr, str):
			expr = strToSympy(expr)
		else:
			raise ValueError("Bad argument for Equation.fromSympy")
		ret = Equation()
		ret.nameDict = nameDict
		nameDict = dict([[v,k] for k,v in nameDict.items()])
		ret.eqSympy = expr
		#ret.eqLatex = sympy.latex(expr.subs(nameDict))
		ret.eqLatex = anythingExceptNumbersToTex(expr.subs(nameDict))
		if PROFILE:
			print(str(millis()-startTime) + " ms for fromSympy")
		return ret
	##Constructs an Equation from a latex equation, a dictionary that matches latex representations to sympy symbols and a list with problematic latexStrings
	##\param texSyms: The script used to generate sympy expressions from latex is a bit buggy, sometimes a symbol in the sympy output has a wrong name. You can prevent this by giving fromLatex the list texSyms that includes all latex strings that may be a problem. eq. Equation.formLatex("U_a", [], {}") returns symbols("U_{a}"), but Equation.formLatex("U_a", ["U_a"], {}") returns symbols("U_a")
	@staticmethod
	def fromLatex(latex, texSyms, nameDict):
		if PROFILE:
			startTime = millis()
		ret = Equation()
		ret.eqLatex = latex
		latex = latex.replace("\\right", "").replace("\\left","").replace("\\,","")
		#texSyms = getAllLatexSymbols(latex)
		#print(texSyms)
		#exit(1)
		#texSyms = [item for item in texSyms if item not in ["\\frac", "\\sqrt", "\\left", "\\right"] ]
		try:
			ret.eqSympy = latex2sympy.latex2sympy(latex, latex2sympy.ConfigL2S()).subs(symbols("pi"),sympy.pi) #TODO brauche ich dne hitnern .subs
		except Exception as err:
			print("Unable to parse LaTeX code. Either the following code is not valid LaTeX, or there is a bug in latex2sympy: ")
			print(latex)
			print("The exception is:")
			print(err)
			exit(1)
		for s in texSyms:
			v = latex2sympy.latex2sympy(s, latex2sympy.ConfigL2S())
			if s != "" and s != "\\pi" and s != str(v) and v in ret.eqSympy.free_symbols:
				nameDict[process_sympy(s)] = s
		ret.eqSympy = ret.eqSympy.subs(nameDict)
		ret.eqSympy = ret.eqSympy.subs(nameDict)
		ret.nameDict = nameDict
		if PROFILE:
			print(str(millis()-startTime) + " ms for fromLatex")
		return ret
	@staticmethod
	def fromSympyAndLatex(sympy, latex, nameDict):
		if isinstance(sympy, str):
			sympy = strToSympy(sympy)
		ret = Equation()
		ret.eqSympy = sympy
		ret.eqLatex = latex
		ret.nameDict = nameDict
		return ret
	#! [Equation showHere]
	##\snippet this Equation showHere
	def showHere(self, label):
		tex("\\begin{equation}")
		tex(self.eqLatex)
		tex("\\label{" + label + "}")
		tex("\\end{equation}")
	#! [Equation showHere]
