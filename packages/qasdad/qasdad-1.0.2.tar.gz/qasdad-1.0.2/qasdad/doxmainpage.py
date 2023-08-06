"""! \mainpage QASDAD
\section TODO
* Use latex2sympy
* Solution to the memName, texName, textName problem: name should be a class
* Document _TEX_FILE_ , _DATA_PATH und _LATEX_PATH_ Dokumentieren
* The only example currently does not work
* Reading large datafiles neads to be faster
* Improving the performance by running pyplot.savefig on a seperate core (don not forget to set the priority levels)
* Document the Executer
* 7.1*hertz*second.evalf() is 7.1*hertz*second this makes Problems if you use calcColumn to calculate a column and Plot() to plot it
* Rewrite latexToSympy
* Use multicolumns to make tables look nicer
* Find a new, cooler name for this project
* Find a new, cooler name for the qasdad executer
* Check whether there are lines where "expr.subs(symbols(str),val)" can be replaced with "expr.subs(str,val)"
* Check whether sympy's Quantity class can be used the improve the way QASDAP handels units
* Compile QASDAP for better performance
* Better Profiling
* PlotLine.fitX should be replaced by PlotLine.fitSym
* PlotLine.fitSym should infer the dimensions of the fitparameters from sympy_fitfunc
* PlotLine.fitSym should accept start values to prevent problems with numerical unstable fitfunctions.
* It is currently not possible to fit multiple functions to the same dataset in the same plot.
* Make a global flag to switch between decimal seperators, maybe by using import locale; locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
* rewrite withoutUnit similar to checkGetUnit
* Make sure that debugTableRaw, debugTableNice and showAsTabular never crash
* niceNumberPrintDigits and niceNumberPrintDelta have trouble showing the numbers ... 0.01, 0.1, 1, 10, 100, 1000, ... The log() calculation of the number of digits should be replaced with a digits in string counting method. Same goes for the number
* showAsTabular should use multicolumns to make sure everything looks nice, even if one value is 2,1\\cdot 10^9 and the other value is 2,1\\cdot 10^10
* showAsTabular should have an option to disable the printing of the uncertainties
* sympy.sympfiy(expr) = expr, if expr is a sympy expression. Use this information to remove a couple lines of code, we do not have to check whether expr is a str or a sympy expression if we just run sympy.sympify.
* The uncertainty of fitparameters and residuum should be stored in PlotLine
* There should be a command PlotLine.texPopt that uses tex() to print all fitparameters, eg.: \\begin{itemize}\\item a = 1,2\\cdot 10^1 m\\item b = 1,24\\cdot 10^1 s\\end{itemize}
* There should be a variable in Column called "prefferedUnit" that makes sure showAsTabular and Plot.showHere prints  [\\Omega] instead of [\\frac V A]
* There should be an easy way to manually change the produced pyOut.tex files, e.g. for the case you want to change the look of the equation for the propagation of uncertainty.
* There should be an option that makes qasdad send informations about it's usuage to my server.
* QASDAD should exit if you attempt to plot multiple things in the same plot with incompatible dimensions.
* Matplotlib has problems showing plots with small errorbars
* Use typecasts to write a cleaner code: There should a function that converts a list, a dictionary or a table to a table.
* Use duck typing to write cleaner code: Equation should have a .subs() method
* QASDAD should come as a pip package, and a latex-package
* QASDAD should run in overleaf
 """
