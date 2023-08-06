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

DATA_PATH = None
def setDataPath(datapath):
	global DATA_PATH
	DATA_PATH = datapath
LATEX_PATH = None
def setLatexPath(latexpath):
	global LATEX_PATH
	LATEX_PATH = latexpath
NO_TEX_PLOT = None
def setNoTexPlot(noTexPlot):
	global NO_TEX_PLOT
	NO_TEX_PLOT = noTexPlot
NO_SAVE_FIG = None
def setNoSaveFig(noSaveFig):
	global NO_SAVE_FIG
	NO_SAVE_FIG = noSaveFig

def listToString(data):
	if data is None:
		return "None"
	ret = "["
	if len(data) != 0:
		ret += str(data[0])
	for i in range(1, len(data)):
		ret += "," + str(data[i])
	ret += "]"
	return ret
	
##Important Element for class Plot, gets stored in Plot.lines. Consists of physical property that gets shown in the Plot and, optionally, a fitcurve.
class PlotLine:
	##Constructor. 
	##Adds line to plot with self.ax.errorbar(xColumn.dataForPlot(), yColumn.dataForPlot(), xerr=xdelta, yerr=ydelta, **kwargs) or
	##self.ax.errorbar(xColumn.dataForPlot(), yColumn.dataForPlot(), xerr=xdelta, yerr=ydelta, label=yColumn.textName(), **kwargs)
	def __init__(self, ax, logFile, xColumn, yColumn, xerr, yerr, **kwargs):
		self.ax = ax
		self.logFile = logFile
		if isinstance(xColumn, np.ndarray):
			self.xcol = Column("", "eq", 1, xColumn, None, None, None)
		else:
			self.xcol = Column(xColumn.memName, xColumn.nameType, xColumn.basicSIUnit, xColumn.rawData, xColumn.specialTexMathName, xColumn.specialTexTextName, xColumn.rawDelta)#We need a deep copy of xColumn, xColumn.rawData and xColumn.rawDelta, because we want to remove all nan's from xColumn.rawData
		if isinstance(yColumn, np.ndarray):
			self.ycol = Column("", "eq", 1, yColumn, None, None, None)
		else:
			self.ycol = Column(yColumn.memName, yColumn.nameType, yColumn.basicSIUnit, yColumn.rawData, yColumn.specialTexMathName, yColumn.specialTexTextName, yColumn.rawDelta)#Aus mir unerklärlichen Gründen ist das eine deep Copy von yColumn.data, also self.ycol.yColumn[0] = 123 verändern nicht yColumn
		#xData = self.xcol.data.copy()
		#yData = self.ycol.data.copy()
		i = 0
		while True:
			if i >= len(self.xcol.rawData):
				break
			if isnan(self.xcol.rawData[i]) or isnan(self.ycol.rawData[i]):
				self.xcol.rawData = np.delete(self.xcol.rawData, i)
				self.ycol.rawData = np.delete(self.ycol.rawData, i)
				self.xcol.rawDelta = np.delete(self.xcol.rawDelta, i)
				self.ycol.rawDelta = np.delete(self.ycol.rawDelta, i)
			else:
				i += 1
		if xerr:
			xdelta = self.xcol.delta
			for i in range(0,len(xdelta)):
				xdelta[i] = withoutUnit(xdelta[i])
		else:
			xdelta = None
		if yerr:
			ydelta = self.ycol.delta
			for i in range(0,len(ydelta)):
				ydelta[i] = withoutUnit(ydelta[i])
		else:
			ydelta = None
		#print(xdelta)
		#print(ydelta)
		#x = [0,1,2,3,4]
		#y = [1,2,3,4,5]
		#yerr = [1,2,1,2,1]
		#self.ax.errorbar(x,y,yerr=yerr)
		#self.ax.errorbar(xColumn.withoutUnit(),yColumn.withoutUnit(), yerr=ydelta)
		#print(xColumn.dataForPlot())
		#print(yColumn.dataForPlot())
		startTime2 = millis()
		logFile.write("xPlt=" + listToString(self.xcol.rawData)+"\n")
		logFile.write("yPlt=" + listToString(self.ycol.rawData)+"\n")
		logFile.write("xdelta=" + listToString(xdelta)+"\n")
		logFile.write("ydelta=" + listToString(ydelta)+"\n")
		if "label" in kwargs:
			logFile.write("ax.errorbar(xPlt, yPlt, xerr=xdelta, yerr=ydelta)\n") #TODO **kwargs soll auch gelogt werden
			self.ax.errorbar(self.xcol.rawData, self.ycol.rawData, xerr=xdelta, yerr=ydelta, **kwargs)
		else:
			logFile.write("ax.errorbar(xPlt, yPlt, xerr=xdelta, yerr=ydelta, label=\"" + self.ycol.textName() + "\")\n") #TODO **kwargs soll auch gelogt werden
			self.ax.errorbar(self.xcol.rawData, self.ycol.rawData, xerr=xdelta, yerr=ydelta, label=self.ycol.textName(), **kwargs)
		if PROFILE:
			print(str(millis()-startTime2) + " ms for errorbar")
		if self.xcol.basicSIUnit != 1:
			logFile.write("ax.set_xlabel(\"" + self.xcol.textName() + " [$" + anythingExceptNumbersToTex(self.xcol.basicSIUnit) + "$]" + "\", usetex="+str(not NO_TEX_PLOT)+")\n")
			self.ax.set_xlabel(self.xcol.textName() + " [$" + anythingExceptNumbersToTex(self.xcol.basicSIUnit) + "$]", usetex=(not NO_TEX_PLOT))
		else:
			logFile.write("ax.set_xlabel(\"" + self.xcol.textName() + "\", usetex="+str(not NO_TEX_PLOT)+")\n")
			self.ax.set_xlabel(self.xcol.textName() , usetex=(not NO_TEX_PLOT))
		if self.ycol.basicSIUnit != 1:
			logFile.write("ax.set_ylabel(\"" + self.ycol.textName() + " [$" + anythingExceptNumbersToTex(self.ycol.basicSIUnit) + "$]" + "\", usetex="+str(not NO_TEX_PLOT)+")\n")
			self.ax.set_ylabel(self.ycol.textName() + " [$" + anythingExceptNumbersToTex(self.ycol.basicSIUnit) + "$]", usetex=(not NO_TEX_PLOT)) #, fontsize=40
		else:
			logFile.write("ax.set_ylabel(\"" + self.ycol.textName() + "\", usetex="+str(not NO_TEX_PLOT)+")\n")
			self.ax.set_ylabel(self.ycol.textName() , usetex=(not NO_TEX_PLOT))
	def fitTest(self, sympy_fitfunc, subsdict, **kwargs): #TOOD: Document this funktion
		if isinstance(sympy_fitfunc, str):
			sympy_fitfunc = strToSympy(sympy_fitfunc)
		elif isinstance(sympy_fitfunc, Equation):
			if str(sympy_fitfunc.eqSympy.lhs) != self.ycol.memName:
				print("bad arguments for fitSym: sympy_fitfunc.lhs != self.ycol.memName")
				print(sympy_fitfunc.eqSympy.lhs)
				print(self.ycol.memName)
				exit(1)
			sympy_fitfunc = sympy_fitfunc.eqSympy.rhs
		sympy_fitfunc = sympy_fitfunc.subs(subsdict)#TODO einheiten checken
		sympy_fitfunc = sympy_fitfunc.subs(symbols(self.xcol.memName), symbols("x"))
		numpy_fitfunc = sympy.lambdify(symbols("x"), subsSIUnitsOne(sympy_fitfunc), "numpy")
		startX = self.xcol.dataForPlot()[0]
		stopX = self.xcol.dataForPlot()[-1]#Performance dataForPlot() gets called multiple times
		xdata = self.xcol.dataForPlot() #TODO das geht doch noch besser
		ydata = numpy_fitfunc(xdata)
		if isinstance(ydata, np.float64):
			#ydata = np.full(len(xdata),self.ycol.withoutUnit()) das war früher hier, aber ich glaube, dass das so falsch ist.
			ydata = np.full(len(xdata),ydata)
		if "label" in kwargs:
			self.ax.plot(xdata, ydata, **kwargs)
		else:
			self.ax.plot(xdata, ydata, label="Test", **kwargs)
	##Uses scipy.optimize.curve_fit to fit the function sympy_fitfunc to the data in self.xColumn and self.yColumn (if you want to know the origin of self.xColumn and self.yColumn look at the documentation of PlotLine.__init__ and Plot.add).
	##This Function is similar to PlotLine.fitSym, but there are 2 differences:
	## * The symbol of the x-asis value in sympy_fitfunc is "x" in fitX but xColumn.memName in fitSym
	## * If sympy_fitfunc is an instance of Equation, fitSym checks whether yColumn.memName and the left hand side of equation match. fitX does not accept an instance of Equation as sympy_fitfunc.
	##Example usuage (linear Fit for a particle that moves at constant speed)
	##\code{.py}
	#object.fitX( "speed*x + offset" , {speed: meter/second, offset: meter} )
	##\endcode
	##optimal fitparameters get stored in plotLine.poptSym and plotLine.poptStr
	##\param sympy_fitfunc Function used to fit. sympy_fitfunc shall only contain "x" and the fitparameters as free symbols. The type of sympy_fitfunc shall be a string or a sympy function
	##\param proposedUnits Sadly, you have to provide a dictionary with the units of every fitparameter. The function checks whether the units are correct. Sadly, only basic SI-Units are allowed.
	##\param **kwargs All additional arguments are passed to matplotlib.pyplot.plot
	def fitX(self, sympy_fitfunc, proposedUnits, **kwargs):
		startTime = millis()
		if isinstance(sympy_fitfunc, str):
			sympy_fitfunc = strToSympy(sympy_fitfunc)
		for i in proposedUnits:
			if subsSIUnitsOne(proposedUnits[i]) != 1:
				print("proposedUnits are not SI Units")
				exit(1)
			if isinstance(i,str):
				proposedUnits[symbols(i)] = proposedUnits.pop(i)
		for s in sympy_fitfunc.free_symbols:
			if s != symbols("x") and s not in proposedUnits:
				print("bad Arguments for fitX: " + str(s) + " is an unknown symbol.")
				print("The expression " + str(sympy_fitfunc) + " shouldn't contain any symbols except for x and the fitparameters:")
				for a in proposedUnits:
					print(a)
				exit(1)
		if checkGetUnit(toBasicSI(sympy_fitfunc.subs(proposedUnits).subs(symbols("x"),self.xcol.unit()))) != checkGetUnit(toBasicSI(self.ycol.unit())):
			print("wrong dimensions in fitfunc:")
			print(str(sympy_fitfunc) + " has dimension " + str(toBasicSI(checkGetUnit(sympy_fitfunc.subs(proposedUnits).subs(symbols("x"),self.xcol.unit())))))
			print("but ycol.unit is " + str(toBasicSI(self.ycol.unit())))
			exit(1)
		all_symbols = [symbols("x")]
		for s in sympy_fitfunc.free_symbols:
			if s != symbols("x"):
				all_symbols.append(s)
		numpy_fitfunc = sympy.lambdify(all_symbols, subsSIUnitsOne(sympy_fitfunc), "numpy")
		popt, pcov = scipy.optimize.curve_fit(numpy_fitfunc, self.xcol.rawData, self.ycol.rawData);
		print(popt)
		print(pcov)
		print(np.sqrt(np.diag(pcov)))
		#startX = self.xcol.dataForPlot()[0]
		#stopX = self.xcol.dataForPlot()[-1]#Performance dataForPlot() gets called multiple times
		#xdata = np.arange(startX,stopX,(stopX-startX)/1000)
		xdata = self.xcol.rawData #TODO das geht doch noch besser
		ydata = numpy_fitfunc(xdata, *popt)
		if not xdata.shape == ydata.shape:
			ydata = np.full(len(xdata),ydata)
		#if isinstance(ydata, np.float64):
		#	#ydata = np.full(len(xdata),self.ycol.withoutUnit()) das war früher hier, aber ich glaube, dass das so falsch ist.
		#	ydata = np.full(len(xdata),ydata)
		if "label" in kwargs:
			self.ax.plot(xdata, ydata, **kwargs)
		else:
			self.ax.plot(xdata, ydata, label="Fit", **kwargs)
		self.poptSym = {}
		self.poptStr = {}
		for i in range(1, len(all_symbols)):
			self.poptSym[all_symbols[i]] = popt[i-1]*proposedUnits[all_symbols[i]]
			self.poptStr[str(all_symbols[i])] = popt[i-1]*proposedUnits[all_symbols[i]]
		if PROFILE:
			print(str(millis()-startTime) + " ms for fitX")
	##Uses scipy.optimize.curve_fit to fit the function sympy_fitfunc to the data in self.xColumn and self.yColumn (if you want to know the origin of self.xColumn and self.yColumn look at the documentation of PlotLine.__init__ and Plot.add).
	##This Function is similar to PlotLine.fitX, but there are 2 differences:
	## * The symbol of the x-asis value in sympy_fitfunc is "x" in fitX but xColumn.memName in fitSym
	## * If sympy_fitfunc is an instance of Equation, fitSym checks whether yColumn.memName and the left hand side of equation match. fitX does not accept an instance of Equation as sympy_fitfunc.
	##Example usuage (linear Fit for a particle that moves at constant speed)
	##\code{.py}
	#object.fitX( "speed*time + offset" , {speed: meter/second, offset: meter} )
	##\endcode
	##optimal fitparameters get stored in plotLine.poptSym and plotLine.poptStr
	##\param sympy_fitfunc Function used to fit. sympy_fitfunc shall only contain the fitparameters and xColumn.memName as free symbols. The type of sympy_fitfunc shall be a string or a sympy function
	##\param proposedUnits Sadly, you have to provide a dictionary with the units of every fitparameter. The function checks whether the units are correct. Sadly, only basic SI-Units are allowed.
	##\param **kwargs All additional arguments are passed to matplotlib.pyplot.plot
	def fitSym(self, sympy_fitfunc, proposedUnits, **kwargs):
		if isinstance(sympy_fitfunc, str):
			sympy_fitfunc = strToSympy(sympy_fitfunc)
		elif isinstance(sympy_fitfunc, Equation):
			if str(sympy_fitfunc.eqSympy.lhs) != self.ycol.memName:
				print("bad arguments for fitSym: sympy_fitfunc.lhs != self.ycol.memName")
				print(sympy_fitfunc.eqSympy.lhs)
				print(self.ycol.memName)
				exit(1)
			sympy_fitfunc = sympy_fitfunc.eqSympy.rhs
		self.fitX(sympy_fitfunc.subs(symbols(self.xcol.memName), symbols("x")), proposedUnits, **kwargs)
##Holds everything necessary to describe one diagramm
class Plot:
	##type(ax) is matplotlib.axes._subplots.AxesSubplot. Calling methods of ax is the recommended way of doing things like making the scale logarithmic, setting label for axes, ...
	ax = None
	#holds values of type PlotLine
	#lines = {}
	##Constructor. Sets self.ax to an instance of the class matplotlib.axes._subplots.AxesSubplot
	logFile = None
	def __init__(self, size=(7,5), display=False, logPath=None): #TODO den display Parameter und den logPath Parameter dokumentieren
		if PROFILE:
			startTime = millis()
		if logPath is not None:
			self.logFile = open(logPath, "w")
		else:
			self.logFile = open(os.devnull, "w")
		self.logFile.write("import matplotlib\n")
		self.logFile.write("import matplotlib.pyplot\n")
		matplotlib.rcParams['text.latex.unicode'] = True
		self.logFile.write("matplotlib.rcParams['text.latex.unicode'] = True\n")
		self.lines = {}
		if display:
			self.fig = matplotlib.pyplot.figure(constrained_layout=True)
			self.logFile.write("fig = matplotlib.pyplot.figure(constrained_layout=True)\n")
		else:
			self.fig = matplotlib.figure.Figure(constrained_layout=True, figsize=size, dpi=1000)
			matplotlib.backends.backend_agg.FigureCanvasAgg(self.fig) #I'm not sure, but this is useless
			self.logFile.write("fig = matplotlib.pyplot.figure(constrained_layout=True, figsize=" + str(size) + ", dpi=1000)\n")
			self.logFile.write("matplotlib.backends.backend_agg.FigureCanvasAgg(fig)\n")
		self.ax = self.fig.add_subplot(111) #alternative: .suplot( instead of .add_suplot(
		self.logFile.write("ax = fig.add_subplot(111)\n")
		#https://matplotlib.org/examples/ticks_and_spines/tick-locators.html
		#https://github.com/matplotlib/matplotlib/issues/8768
		#https://github.com/matplotlib/matplotlib/pull/12865
		if PROFILE:
			print(str(millis()-startTime) + " ms for Plot.__init__")
	##\snippet this Plot add
	def add(self, xColumn, yColumn, lineName = "default", xerr=False, yerr=False, **kwargs):
		if PROFILE:
			startTime = millis()
		#! [Plot add]
		self.lines[lineName] = PlotLine(self.ax, self.logFile, xColumn, yColumn, xerr, yerr, **kwargs)
		#! [Plot add]
		if PROFILE:
			print(str(millis()-startTime) + " ms for Plot.add")
	##Saves the plot in a file
	##\param path Filepath of the graph. Has to include a correct file extension.
	def writeToFile(self, path):
		if PROFILE:
			startTime = millis()
		#self.ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
		#self.ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
		#self.ax.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		#self.ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		self.ax.legend()
		self.fig.savefig(path)
		if PROFILE:
			print(str(millis()-startTime) + " ms for Plot.writeToFile")
	##Saves the plot as a png and runs tex("\includegraphics[width=size\\textwidth]{path}"). **kwargs are passed to self.ax.legend
	def showHere(self,size=1.0, **kwargs):
		if NO_SAVE_FIG:
			return
		if PROFILE:
			startTime = millis()
		#self.ax.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		#self.ax.yaxis.set_major_locator(matplotlib.ticker.AutoLocator())
		self.ax.legend(**kwargs)
		for i in range(0,100):
			plot_path = os.path.join(DATA_PATH, str(i) + ".pdf") #.png does not work on my laptop
			if not os.path.exists(plot_path):
				self.logFile.write("fig.savefig('" + plot_path + "')")
				self.fig.savefig(plot_path)
				tex("\\includegraphics[width=" + str(size) + "\\textwidth]{" + os.path.relpath(plot_path,start=os.path.dirname(LATEX_PATH))  +"}\\\\" )
				if PROFILE:
					print(str(millis()-startTime) + " ms for Plot.showHere")
				return
		print("unable to safe plot")
		exit(1)
	#! [Plot showAsFigure]
	##\snippet this Plot showAsFigure
	def showAsFigure(self, label, caption, size=1.0, **kwargs):
		tex("\\begin{figure}[H]")
		tex("\\centering")
		self.showHere(size, **kwargs)
		tex("\\caption{" + caption + "}")
		tex("\\label{" + label + "}")
		tex("\\end{figure}")
	#! [Plot showAsFigure]
	#! [Plot getitem]
	##\snippet this Plot getitem
	def __getitem__(self, key):
		return self.lines[key]
	#! [Plot getitem]
