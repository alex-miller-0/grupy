## grupy_in object

import sys
import os


class grupy_in:
	
	def __init__ (self, 
				  dir, # directories of calculations (input file)
				  hs_path,  # high symmetry path (input file)
				  hs_points, # high symmetry points and labels
				  sg, #space group (input file)
				  prefix, # calculation name( get from calculations)
				  nat,	# number of atoms (get from calculations)
				  V, # volume array (get from calculations)
				  m, # atomic mass array ( get from calculation)
				  modes,
				  path,  # make from high symmetry path
				  q, # list of q points (get from calculations)
				  ):
		
		self.dir = dir
		self.hs_path = hs_path
		self.hs_points = hs_points
		self.sg = sg
		self.prefix = prefix
		self.nat = nat
		self.V = V
		self.m = m
		self.modes = modes
		self.path = path
		self.q = q