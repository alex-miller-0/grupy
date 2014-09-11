__author__ = 'alex-admin'

import xml.etree.ElementTree as et
import os

def XMLparse (dirs):

    def GetPrefix(cwd):
        for f in os.listdir("%s/%s/_ph0"%(cwd, dirs[0])):
            if f.endswith(".save"):
                return str(f[:-5])

    def GetVec(e):
        e = e.split()
        return [float(i) for i in e]


    d = os.getcwd()
    V = []
    prefix = GetPrefix(d)
    M = []
    N = 0


    for X in range(len(dirs)):

        A1, A2, A3, B1, B2, B3, masses = ([] for i in range(7))
        nat = 0

        # Read the file named rf (it is data-file.xml)
        rf = ""

        # Look for the file
        if os.path.isdir('%s/%s/_ph0/%s.save'%(d,dirs[X],prefix)):
            if os.path.exists('%s/%s/_ph0/%s.save/data-file.xml'%(d, dirs[X], prefix)):
                rf = '%s/%s/_ph0/%s.save/data-file.xml'%(d,dirs[X],prefix)
        elif os.path.isdir('%s/%s/%s.save'%(d, dirs[X], prefix)):
            if os.path.exists('%s/%s/%s.save/data-file.xml'%(d, dirs[X], prefix)):
                rf = '%s/%s/%s.save/data-file.xml'%(d,dirs[X], prefix)
            else:
                import sys
                print "Cannot find data-file.xml. It should be in _ph0/prefix.save or prefix.save"
                sys.exit()
        elif os.path.exists('%s/%s/data-file.xml'%(d, prefix)):
            rf = '%s/%s/data-file.xml'%(d, prefix)

        else:
            import sys
            print "Cannot find _ph0 or prefix.save directories"
            sys.exit()

        tree = et.parse(rf)

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

            #Note: this is pulling the masses out exactly as you put them in so make sure they're accurate!
            elif "SPECIE." in elem.tag:
                n = int(elem.tag[-1:])
                for x in elem.iter():
                    if x.tag == "MASS":
                        masses[n-1] = float(x.text)*911.444242132
        M=masses
        N = nat
        import numpy as np
        V.append(np.dot(np.cross(A1,A2),A3))



    return prefix, V, M, N