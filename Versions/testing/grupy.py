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


# Parse options to graph data and to make/run q2r.in and matdyn.in scripts

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



# Grupy

# Welcome to grupy!
print "\n!-----------   grupy! version 1.3   -----------!\n"

# Generate the input object
Gin = GrupyIn()
Gin.GrupyInput()

# grupy --make
if options.make_scripts:
    MakeMatdyn(Gin.dir, Gin.prefix, Gin.path, Gin.m)
    MakeQ2r(Gin.prefix, Gin.dir)
    print "\nq2r.in and matdyn.in files created\n"
    sys.exit()

# grupy --run
if options.run_scripts:

    for i in range(len(Gin.dir)):
        q = 'cd %s && q2r.x < q2r.in && cd ..' % (Gin.dir[i])
        sub.call(q, shell=True)

        m = 'cd %s && matdyn.x < matdyn.in && cd ..' % (Gin.dir[i])
        sub.call(m, shell=True)

        print "dynamical matrix files created"
    sys.exit()


# grupy
omega = ReadModes(Gin.nat, Gin.m, Gin.dir, units)

# Gruneisen
if not options.bands and not options.avg:

    # Make a copy of the frequency dictionary so that two routes can use it
    import copy
    p = copy.deepcopy(omega)

    # Get mode Gruneisens, q points, and reduced path (also get phonons for acoustic mode finding)
    phonons = Phonons(p, Gin.BZ_path, Gin.path)
    gruneisen = Gruneisen(omega, Gin.V, Gin.BZ_path, Gin.path, Gin.nat)

    if Gin.path:
        Gout = GrupyOut(Gin)
        Gout.Gruneisen(phonons, gruneisen)
        Gout.units = units
    #else:
    #    bands = GetBands(Gin, units)

    WriteGrupyFile(Gout, Gin, 0)
    print "\ngrupy.out file written\n"



# Phonon dispersion
if options.bands:

    # Get the frequencies, q points, and reduced path
    phonons = Phonons(omega, Gin.BZ_path, Gin.path)

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
        phonons = [phonons[index]]

    if Gin.path:

        Gout = GrupyOut(Gin)
        Gout.Phonons(phonons)
        Gout.units = units

    #else:
    #    Gout = grupy_out(Gin.prefix, None, bands, mode_index, group_velocity, None, acoustic,units)


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
