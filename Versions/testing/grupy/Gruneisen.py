__author__ = 'asmiller'
import sys

def Phonons(omega, reducedQ, qPoints):
    for i in range(len(omega)):
        for j in range(len(omega[i])):
            omega[i][j]['reducedQ'] = reducedQ[j]
            omega[i][j]['cartQ'] = qPoints[j]
    return omega



# Calculate the Gruneisen parameter using a simple finite difference
def FinDiffOm(om):
    D = {}
    for key in om[0].keys():
        D[key] = float(om[len(om)-1][key]) - float(om[0][key])

    return D

def G(omega, dOmega, V, dV):
    if round(omega, 8) == 0:
        return 0
    g = -(dOmega/(2*omega))*(V/dV)
    return g

def Gruneisen(omega, V, reducedPath, qPoints, nat):
    gruneisen = []
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
            g = {'reducedQ':reducedPath[i], 'cartQ':qPoints[i], 'Gruneisen':{}}

            # Iterate through the calculations
            for j in range(len(omega)):
                tmpOm.append(omega[j][i])

            # Get the del(Omega) values at this q point
            dOmega = FinDiffOm(tmpOm)

            # Iterate through the modes (3N)
            for k in range(3*nat):

                Om = float(omega[eq_i][i]['%s'%(k+1)])
                dOm = float(dOmega['%s'%(k+1)])
                #if i==60:
                #    print omega[eq_i][i]
                g['Gruneisen']['%s'%(k+1)] = G(Om, dOm, float(V[eq_i]), dV)

            gruneisen.append(g)

    return gruneisen







