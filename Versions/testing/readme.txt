grupy readme:

Written by Alex Miller in 2014 at the University of Texas.


OVERVIEW:

Grupy is capable of calculating and plotting the Gruneissen parameter for a material across a dispersion of q-points (i.e. the Brillouin zone). This is a post-processing program that requires a phonon dispersion calculation to first be performed using Quantum Espresso. Grupy is written in Python, which means you need to install python before using it. You will also need numpy and matplotlib libraries.

INSTALLATION:
1) Install python, numpy, and matplotlib
2) Change to the directory containing setup.py.
3) Run python setup.py install
	Note: if you wish to install grupy to a particular directory (i.e. not
	      the default Python directory) use the option --prefix="path_to_directory"

BEFORE USE:
Grupy consists of two scripts: grupy and gruplot. Before using grupy, you must run three
separate phonon calculation in Quantum Espresso. These must be a dispersion calculations (ldisp=.true.). One calculation is performed at the relaxed (equilibrium) volume. Another is run at some volume slightly smaller than equilibrium. A third is run at some volume slightly larger than equilibrium. It is recommended these volumes be ~1% below and above equilibrium volume, respectively.

Place these three calculations in one directory with the following structure.

	       |--- smaller volume calculation
parent folder--|--- equilibrium volume calculation
	       |--- larger volume calculation


USING GRUPY:
1) Write a grupy.in with the following information and place it in the parent folder shown above:
DIRS = names of folders containing calculations with spaces between the names
SPACE_GROUP = number space group of structure
PATH 'symmetry point 1' q-vector 1   'symmetry point 2' q-vector 2   etc

Notice that PATH does not have an equals sign. An example is:
PATH   G 0 0 0    X 0 1 0    W 0.5 1 0 


2) Now you are all set up. Assuming you have the grupy scripts directory in your path, run the following:

	a) Make the q2r.x and dynmat.x scripts:
		grupy --make

	b) Run those scripts:
		grupy --run

	c) Run grupy:
		grupy

This will create a file called prefix.grupy.out, where prefix is the name of your material. This contains a dispersion of Gruneissen parameter along the path specified in grupy.in for each mode in your material.

As an alternative to part c, you can run grupy --bands to create a file called prefix.grupy.bands.out, which contains the phonon dispersion for each of the three calculations you performed.





