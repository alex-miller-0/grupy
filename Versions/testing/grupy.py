#!/usr/bin/python
import os
import sys

# # append path to grupy modules
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd, ".."))

from grupy import *
from grupy.qe import *
from grupy.velocity import *
from optparse import OptionParser
import subprocess as sub


# Welcome to grupy!
print "\n!-----------   grupy! version 1.2.1   -----------!\n"


# should eventually write some flags for bad data input
## From input file
##################

dir, in_path, temps = GetInput()


## Parse options to graph data and to make/run q2r.in and matdyn.in scripts 
###########################################################################

parser = OptionParser()
parser.set_defaults(
    make_scripts=False,
    run_scripts=False,
    bands=False,
    single=False,
    avg=False,
    cm=False)

parser.add_option("--make", dest="make_scripts", action="store_true")
parser.add_option("--run", dest="run_scripts", action="store_true")
parser.add_option("--bands", dest="bands", action="store_true")
parser.add_option("-s", dest="single", action="store")  #plot a phonon bands structure without needing 3 calculations
parser.add_option("--avg", dest="avg", action="store_true")
parser.add_option("--cm", dest="cm", action="store_true")

(options, args) = parser.parse_args()

units = "thz"
if options.cm == True:
    units = "cm-1"


#### grupy_in object
####################
Gin = grupy_in(dir, in_path, None, None, None, None, None, None, None, None, None)
Gin.prefix, Gin.V, Gin.m, Gin.nat = XMLparse(Gin.dir)

if Gin.in_path:
    Gin.path, Gin.hs_points = MakePath(Gin.in_path)
else:
    "No path selected: I will calculate average Gruneisen parameter."

# Old ways of getting these; think I will delete soon
#Gin.prefix = GetPrefix(Gin.dir)
#(Gin.nat, Gin.V, Gin.m) = GetNat_M_V(Gin.dir, Gin.prefix)

if options.make_scripts:
    MakeMatdyn(Gin.dir, Gin.prefix, Gin.path, Gin.m)
    MakeQ2r(Gin.prefix, Gin.dir)
    print "\nq2r.in and matdyn.in files created\n"
    sys.exit()

# this doesn't work - I need to write a shell script
if options.run_scripts:

    for i in range(len(Gin.dir)):
        q = 'cd %s && q2r.x < q2r.in && cd ..' % (Gin.dir[i])
        sub.call(q, shell=True)

        m = 'cd %s && matdyn.x < matdyn.in && cd ..' % (Gin.dir[i])
        sub.call(m, shell=True)

        print "dynamical matrix files created"
    sys.exit()




if Gin.path:
    ## Generate the BZ path and corresponding high symmetry labels
    Gin.BZ_path, BZ_labels = MakeBZPath(Gin.hs_points, Gin.path)


## Get the data from QE output text files
q, Darray = ReadDynMat(Gin.nat, Gin.m, Gin.dir)


## Format the data to be written to a formatted output file
Gin.q, gru_data, mode_index, omega_eq, acoustic = GruCalc(Gin, q, Darray)
print len(q), len(Gin.q)




'''
FIND index in q of Gamma point (0,0,0) and match that with the index of Gin.q
    -> find which frequencies = 0 in GruCalc at the same index

'''






# noinspection PyInterpreter
if not options.bands and not options.avg:
    if Gin.path:
        Gout = grupy_out(Gin.prefix, BZ_labels, gru_data, mode_index, None, omega_eq, acoustic,units)

    else:
        bands = GetBands(Gin)

        Gout = grupy_out(Gin.prefix, None, gru_data, mode_index, None, bands[0], acoustic, units)
    WriteGrupyFile(Gout, Gin, 0)
    print "\ngrupy.out file written\n"



### need to feed in new BZ_path
if options.bands:

    if options.single:
        # Match a variable in Gin.dir list with the directory supplied with the -s option
        if options.single not in Gin.dir:
            print "\nCalculation is not in the current directory. Exiting.\n"
            sys.exit()

        index = None
        for i in range(len(Gin.dir)):
            if str(Gin.dir[i]) == str(options.single):
                index = i

        #Recreate lists of single items for Gin variables
        Gin.dir = [Gin.dir[index]]
        Gin.V = [Gin.V[index]]




    bands = GetBands(Gin, options.cm)

    group_velocity = GetGroupVelocity(bands)
    if Gin.path:
        Gout = grupy_out(Gin.prefix, BZ_labels, bands, mode_index, group_velocity, None, acoustic,units)
    else:
        Gout = grupy_out(Gin.prefix, None, bands, mode_index, group_velocity, None, acoustic,units)


    WriteGrupyFile(Gout, Gin, 1)
    print "\ngrupy.bands.out file written\n"


## Calculate the average Grunesien parameter AFTER writing appropriate grupy.out file
if options.avg:
    print "Material: %s"%Gin.prefix
    from grupy.avg import avg
    gru_avg = avg(Gin,temps)

    for i in range(len(gru_avg)):
        print "\nTemperature (K): ",gru_avg[i]['temperature (K)']
        print "Cv: ",gru_avg[i]['Cv']
        print "Average Gruneisen parameter:  ",gru_avg[i]['average Gruneisen']
        print ""
    print "----------------------------------"
