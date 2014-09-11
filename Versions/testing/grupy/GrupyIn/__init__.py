# # grupy_in object

import sys
import os
from XMLparse import *
from ReadInput import *
from MakePath import MakePath
from MakeBZPath import MakeBZPath


class GrupyIn:
    def __init__(self):
        self.dir = None
        self.in_path = None
        self.hs_points =None
        self.prefix = None
        self.nat = None
        self.V = None
        self.m = None
        self.BZ_path = None
        self.modes = None
        self.path = None
        self.q = None
        self.BZ_labels = None



    def QE(self):
        self.prefix, self.V, self.m, self.nat = XMLparse(self.dir)

    def GrupyInput(self):
        self.dir, self.in_path, self.temps = ReadInput()
        self.QE()
        if self.in_path:
            self.path, self.hs_points = MakePath(self.in_path)
            self.BZ_path, self.BZ_labels = MakeBZPath(self.hs_points, self.path)
        else:
            print "No path selected."
