# # grupy_out object

import sys
import os
'''
def GetAcousticModes (acoustic,q_labels):
         for key in acoustic:
            for label in range(len(q_labels)):
                if str(q_labels[label][1])[0:12] == key[0:12]:
                    for i in range(len(acoustic[key])):
                        acoustic[key][i] = int(acoustic[key][i])
                    return acoustic[key]
'''
class grupy_out:

    def __init__(self,
                 prefix,
                 q_labels,  # high symmetry labels (from database)
                 gru_data,  # data matrix (from GruCalc)
                 mode_index,  # want to make sure we know which mode is which
                 group_velocity,
                 omega_eq,
                 acoustic,
                 units

    ):
        self.prefix = prefix
        self.q_labels = q_labels
        self.gru_data = gru_data
        self.mode_index = mode_index
        self.group_velocity = group_velocity
        self.omega_eq = omega_eq
        #self.acoustic_i = GetAcousticModes(acoustic,q_labels)
        self.acoustic_i = acoustic
        self.units = units




