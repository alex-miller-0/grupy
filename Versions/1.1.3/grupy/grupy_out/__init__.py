## grupy_out object

import sys
import os


class grupy_out:
	
	def __init__ (self, 
				  prefix, 
				  q_labels, # high symmetry labels (from database)
				  gru_data, # data matrix (from GruCalc)
				  mode_index, # want to make sure we know which mode is which
				  group_velocity
					):
		self.prefix = prefix
		self.q_labels = q_labels
		self.gru_data = gru_data
		self.mode_index = mode_index
		self.group_velocity = group_velocity