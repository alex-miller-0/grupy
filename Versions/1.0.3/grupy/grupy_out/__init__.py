## grupy_out object

import sys
import os


class grupy_out:
	
	def __init__ (self, 
				  prefix, 
				  q_labels, # high symmetry labels (from database)
				  gru_data # data matrix (from GruCalc)
					):
		self.prefix = prefix
		self.q_labels = q_labels
		self.gru_data = gru_data
		