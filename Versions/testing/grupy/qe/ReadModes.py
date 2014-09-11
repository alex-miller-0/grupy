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

def SortModes(vec,val,evec,nat):
    evals = {}

    for i in range(3*nat):
        tmpDot = 0.0
        tmpMode = 0
        dottedModes = []
        for j in range(3*nat):

            # numpy.vdot is used for complex vectors (numpy.dot won't give the proper Kroneker products here)
            d = np.abs(np.vdot(np.array(vec[i]), np.array(evec['%s'%(j+1)]).T))


            if d > tmpDot:
                if '%s'%(j+1) not in evals and (j+1) not in dottedModes:
                    evals['%s'%(j+1)] = val[i]

                    tmpDot = d
                    dottedModes.append(tmpMode)


    return dict(sorted(evals.items()))


def ReadModes(nat, amass, dir, units):
    c=1
    # Units are in THZ. Multiple by a constant to get cm-1 or some other units
    if units == "thz":
        c = 1
    elif units =="cm-1":
        c = 33.35649629


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
        evec = {} # The previous eigenvector. Used to sort modes.
        # NOTE: because of numerical noise, you cannot dot every new eigenvector with the first one; you have
        #   to dot it with the LAST eigenvector and make a new one for the next q point

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
                            #if len(q)==1:
                            evec['%s'%tmpMode] = ev


                        s = line.split()
                        thz = s[3]
                        cm = s[6]
                        val.append(float(thz)*c)
                        tmp = i+1
                        #if len(q)==1:
                        tmpMode = s[1][0]
                        tmpVec = []

                    if i-tmp < nat and i+1-tmp>0 and tmp!=0:
                        s = line.split()
                        tmpVec.append(s)

                    if "***" in line and tmp!=0:
                        tmp = 0
                        ev = BuildEvec(tmpVec)
                        vec.append(ev)

                        #if len(q)==1:
                        evec['%s'%tmpMode] = ev
                        #Check if this is the first evec. If so, put it in evec. If not, dot it w/ evec to sort modes

                        sorted = SortModes(vec,val,evec,nat)
                        eval[x].append(sorted)

                        tmpVec = None
                        vec = []
                        val = []


    return eval








