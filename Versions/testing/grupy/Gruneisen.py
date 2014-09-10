__author__ = 'asmiller'
import sys


def FinDiffOm(om):
    D = {}
    for key in om[0].keys():
        d = 0
        for i in range(1,len(om)):
            #print key
            d+= (float(om[i][key]) - float(om[i-1][key])) /2.
        D[key] = d/(len(om)-1)
    return D

def G(omega, dOmega, V, dV):
    g = -(dOmega/(2*omega))*(V/dV)
    return g

def Gruneisen(omega, V):
    n = len(omega)
    if n%2 == 0:
        print "ERROR: You don't have an odd number of calculations! Exiting..."
    else:
        # The equilibrium calculation should be the one in the center of the list in grupy.in
        eq_i = len(V)/2

        # Iterate through all q points
        dV = V[len(V)-1] - V[0]
        for i in xrange(len(omega[0])):
            tmpOm = []
            tmpV = []

            # Iterate through the calculations
            for j in range(len(omega)):
                tmpOm.append(omega[j][i])

            dOmega = FinDiffOm(tmpOm)
            gruneisen = G(omega[eq_i][i], dOmega, float(V[eq_i]), dV)








