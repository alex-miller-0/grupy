__author__ = 'asmiller'
import sys

def FinDiff(om)
    d = 0.
    for i in range(len(om)):
        d+= om
    return d

def Gruneisen(omega, V):
    n = len(omega)
    if n%2 == 0:
        print "ERROR: You don't have an odd number of calculations! Exiting..."
    else:
        median = n/2

        # Iterate through all q points
        for i in xrange(len(omega[0])):
            tmpOm = []
            tmpV = []
            for m in range(median):
                tmp.append(omega[m][i])

            dOmega = FinDiff(tmp)




