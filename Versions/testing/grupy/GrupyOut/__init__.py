__author__ = 'asmiller'

# # grupy_out object

import sys
import os

class GrupyOut:

    def __init__(self, Gin):
        self.prefix = Gin.prefix
        self.q_labels = Gin.BZ_labels
        self.calc = Gin.dir
        self.V = Gin.V
        self.phonons = None
        self.gruneisen = None
        self.group_velocity = None
        self.acoustic = None
        self.units = None

    def GetAcousticModes(self,ph):
        acoustic = []
        for i in range(len(ph)):
            acoustic.append([])
            for j in range(len(ph[i])):
                if ph[i][j]['cartQ'] == [0,0,0]:
                    for key in ph[i][j].keys():
                        if len(str(key)) == 1:
                            if float(ph[i][j][key]) == 0:
                                if int(key) not in acoustic[i]:
                                    acoustic[i].append(int(key))
        self.acoustic = acoustic

    def Phonons(self,ph):
        self.GetAcousticModes(ph)
        self.phonons = ph

    def Gruneisen(self,ph,gr):
        self.GetAcousticModes(ph)
        self.phonons = ph
        self.gruneisen = gr
