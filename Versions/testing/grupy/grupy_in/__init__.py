# # grupy_in object

import sys
import os


class grupy_in:
    def __init__(self,
                 dir,  # directories of calculations (input file)
                 in_path,  # high symmetry path (input file)
                 hs_points,  # high symmetry points and labels
                 prefix,  # calculation name( get from calculations)
                 nat,  # number of atoms (get from calculations)
                 V,  # volume array (get from calculations)
                 m,  # atomic mass array ( get from calculation)
                 BZ_path,
                 modes,
                 path,  # make from high symmetry path MAY NOT NEED THIS
                 q,  # list of q points (get from calculations)
    ):
        self.dir = dir
        self.in_path = in_path
        self.hs_points = hs_points
        self.prefix = prefix
        self.nat = nat
        self.V = V
        self.m = m
        self.BZ_path = BZ_path
        self.modes = modes
        self.path = path
        self.q = q