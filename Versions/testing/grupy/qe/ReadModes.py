__author__ = 'asmiller'
import os
import numpy as np

def BuildEvec(tVec):
    vec = []
    for i in range(len(tVec)):
        # Remove parentheses
        tVec[i] = tVec[i][1:-1]
        for k in range(len(tVec[i])):
            if k%2==0 or k==0:
                #print float(tVec[i][k]), tVec[i][k+1]
                vec.append(float(tVec[i][k])+float(tVec[i][k+1])*1j)
    return vec

def SortModes(vec,val,evec):
    evals = {}
    #print np.absolute(np.dot(vec[0],evec['1']))

    for i in range(len(vec)):
        tmpDot = 0
        tmpMode = 0
        for j in range(len(vec)):

            # numpy.vdot is used for complex vectors (numpy.dot won't give the proper Kroneker products here)
            d = np.absolute(np.vdot(np.array(vec[i]), np.array(evec['%s'%(j+1)]).T))

            if d>tmpDot:
                tmpDot = d
                tmpMode = j+1

        evals['%s'%tmpMode] = val[i]

    return evals


def ReadModes(nat, amass, dir):
    # Note: QE produces atomic masses in a weird unit
    # They are first extracted from prefix.dyn1


    eval = []  # Eigenvalues

    cwd = os.getcwd()

    for x in xrange(len(dir)):

        start = 0
        end = 0
        qcount = 0
        m1 = 0
        m2 = 0
        row = 0
        col = 0
        incount = 0
        q = []
        eval.append([])
        evec = {} # Just the first eigenvector. More will be built and dotted to sort modes.

        for file in os.listdir("%s/%s/" % (cwd, dir[x])):

            if file.endswith("matdyn.modes"):

                name = "%s/%s/%s" % (cwd, dir[x], file)
                f = open(name, 'r')
                tmp = 0
                vec = []
                val = []
                tmpVec = None
                tmpMode = None
                for i, line in enumerate(f):

                    if "q" in line and "=" in line:
                        qcount += 1
                        start = i + 2
                        end = i + 2 + (4 * nat * nat)
                        temp = line.split()
                        q.append([temp[2], temp[3], temp[4]])

                    if "omega" in line:
                        if tmpVec != None:
                            ev = BuildEvec(tmpVec)
                            vec.append(ev)
                            if len(q)==1:
                                evec['%s'%tmpMode] = ev


                        s = line.split()
                        thz = s[3]
                        cm = s[6]
                        val.append(thz)
                        tmp = i+1
                        if len(q)==1:
                            tmpMode = s[1][0]
                        tmpVec = []

                    if i-tmp < nat and i+1-tmp>0 and tmp!=0:
                        s = line.split()
                        tmpVec.append(s)

                    if "***" in line and tmp!=0:
                        tmp = 0
                        ev = BuildEvec(tmpVec)
                        vec.append(ev)

                        if len(q)==1:
                            evec['%s'%tmpMode] = ev
                        #Check if this is the first evec. If so, put it in evec. If not, dot it w/ evec to sort modes

                        sorted = SortModes(vec,val,evec)
                        eval[x].append(sorted)

                        tmpVec = None
                        vec = []
                        val = []


    return eval








