#!/usr/bin/python
import os
import sys

## append path to grupy modules
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append( os.path.join( cwd, "..") )

from grupy.gruplot import *
from optparse import OptionParser

parser = OptionParser()
parser.set_defaults( 
					 bands = None)


parser.add_option("--bands", dest="bands", action="store")

(options, args) = parser.parse_args() 

type = ""
volume = None


if options.bands:
	type = "bands"
	calc = options.bands  # this is the specific calculation you ran
						 	 # corresponding to a particular volume

else:
	type = "gru"
	calc = None


prefix, labels, data = GetGrupyData(type, calc)

GruPlot(prefix, labels, data)

