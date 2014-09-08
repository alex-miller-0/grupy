__author__ = 'alex-admin'

import xml.etree.ElementTree as et
def XMLparse (dirs):

    def GetPrefix():
        import os
        for f in os.listdir("./%s/_ph0"%dirs[0]):
            if f.endswith(".save"):
                return str(f[:-5])

    def GetVec(e):
        e = e.split()
        return [float(i) for i in e]



    V = []
    prefix = GetPrefix()
    M = []
    N = 0


    for X in range(len(dirs)):

        A1=[]
        A2 = []
        A3 = []
        B1 = []
        B2 = []
        B3 = []
        masses = []
        nat = 0

        tree = et.parse('%s/_ph0/%s.save/data-file.xml'%(dirs[X],prefix))
        root = tree.getroot()
        for elem in root.iter():
            if elem.tag=="a1":
                A1 = GetVec(elem.text)
            elif elem.tag=="a2":
                A2 = GetVec(elem.text)
            elif elem.tag=="a3":
                A3 = GetVec(elem.text)

            elif elem.tag == "b1":
                B1 = GetVec(elem.text)
            elif elem.tag == "b2":
                B2 = GetVec(elem.text)
            elif elem.tag == "b3":
                B3 = GetVec(elem.text)

            elif elem.tag == "NUMBER_OF_ATOMS":
                nat = int(elem.text)
                for i in range(nat):
                    if len(masses) < nat:
                        masses.append(0.)

            elif "SPECIE." in elem.tag:
                n = int(elem.tag[-1:])
                for x in elem.iter():
                    if x.tag == "MASS":
                        masses[n-1] = float(x.text)
        M=masses
        N = nat
        import numpy as np
        V.append(np.dot(np.cross(A1,A2),A3))



    return prefix, V, M, N