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

#This file only contains dead code that is not active but may be activated in further version
#@cond INTERNAL
def getAllLatexSymbols(latex): #TODO talk with the guy who wrote latex2Sympy
	#print(latex)
	splits = [" ", "\t", "\n", "{", "}", "(", ")", "=", "*", "/", "+", "-"]
	allSyms = []
	start = 0
	lastSymPos = 0
	#for i in range(0, len(latex)):
	i = 0
	while i < len(latex):
		#print("########################")
		#print(latex[i:i+5])
		if latex[i] in splits:
			if start != i:
				allSyms.append(latex[start:i])
				lastSymPos = i
			start = i+1
		elif latex[i] == "\\":
			if start != i:
				allSyms.append(latex[start:i])
				lastSymPos = i
			start = i
		elif latex[i] == "_" or latex[i] == "^":
			#print("====================")
			#print(latex[i:i+5])
			lastStart = i 
			#print("lastStart:", latex[lastStart:lastStart+5])
			while latex[lastStart] in splits or latex[lastStart] == "_" or latex[lastStart] == "^" :
				#print("char:", latex[lastStart])
				lastStart -= 1
			if latex[i-1] in splits:
				lastStart -= len(allSyms[-1])-1
			#print("lastStart:", latex[lastStart:lastStart+5])
			if latex[i-1] in splits:
				allSyms.pop()
			#lastStart = lastSymPos
			depth = 0
			quote = False
			alreadyHadSomething = False
			while depth != 0 or not alreadyHadSomething:
				i += 1
				if latex[i] == "\"" or latex[i] == "\'":
					quote = not quote #TODO a_\text{"\" "} würde probleme machen
				elif not quote and latex[i] == "{":
					depth += 1
				elif not quote and latex[i] == "}":
					depth -= 1
				elif not latex[i] in splits:
					alreadyHadSomething = True
			i += 1
			allSyms.append(latex[lastStart:i])
			lastSymPos = i
			start = i
			#print("end of _ or ^")
		i += 1
	if start != len(latex):
		allSyms.append(latex[start:])
	return allSyms
#@endcond INTERNAL
#print(getAllLatexSymbols("a   b_1"))
#print(getAllLatexSymbols("a   b _1"))
#print(getAllLatexSymbols("a   U_a/U_b"))
#exit(1)
