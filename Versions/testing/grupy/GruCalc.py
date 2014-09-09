# #diagonalize
import numpy as np
from qe.ReadDynMat import *
import cmath


def Get_Eval_Evec_dDdV(Darray, BZ_path):

    #Deq = []   ## equilibrium dyn matrices
    Dn = []  ## non-equilibrium dyn matrices
    dD = []  ## what will be returned (dD/dV)
    EVAL = []  ## eigenvalues (omega^2)
    EVEC = []  ## eigenvectors that diagonalize eq matrices

    for i in range(len(Darray)):  # 3

        if i != 0:  ## i.e. not an equilibrium matrix

            Dn.append([])

        for j in xrange(len(Darray[i])):  # number of q points

            if i == 0:  ## again, just looking at equilibrium matrices

                EVAL.append([])
                EVEC.append([])

                eval, evec = np.linalg.eigh(Darray[i][j])

                #Deq.append ( Darray[0][j] )

                for k in xrange(len(eval)):  # 3N
                    # TESTING: should be 3N now
                    EVAL[j].append(eval[k])
                    EVEC[j].append(evec[k])



            else:  ## i.e. NON-equilibrium matrices
                Dn[i - 1].append(Darray[i][j])  ## this is a full dyn matrix


    # Dn array should have 2 columns of elements (for + and - volume calculations)
    #	, with each element being a 3Nx3N matrix of eigenvalues at that q-point
    # Deq array should have three dimensions

    if Dn:
        for i in xrange(len(Darray[0])):  # q points
            dD.append([])
            for j in xrange(len(Darray[0][i])):  # 3N
                dD[i].append([])

                for k in xrange(len(Darray[0][i][j])):  # 3N

                    # Dn[0] is D+ , Dn[1] is D-
                    dD[i][j].append((Dn[0][i][j][k] - Dn[1][i][j][k]))


    return EVAL, EVEC, dD


## Calculate Gruneisen parameter

def GruCalc(Gin, q, Darray):
    V = Gin.V
    nat = Gin.nat
    amass = Gin.m
    BZ_path = Gin.BZ_path
    acoustic = {}


    # get equilibrium eigenvalues, equilibrium eigenvectors, and dD (nonequilibrium differences) matrix
    eval_eq, evec_eq, dD = Get_Eval_Evec_dDdV(Darray, BZ_path)  # get equilibrium eigenvalues

    dD = np.asarray(dD)
    evec_eq = np.asarray(evec_eq)

    gru = []  # the Gruneisen parameter
    gru_i = []  # the mode index of said Gruneisen parameter
    omega_i=[]

    gru.append([])  # for the q point column
    gru_i.append([])
    omega_i.append([])


    for i in xrange(len(eval_eq)):  # should be equal to the number of q points

        if BZ_path:
            gru[0].append(BZ_path[i])
            gru_i[0].append(BZ_path[i])
            #omega_i[0].append(None)
            omega_i[0].append(BZ_path[i])
        else:
            gru[0].append(i)
            gru_i[0].append(i)
            omega_i[0].append(i)


        # SORTING of eigenvalues: must correspond to eigenvectors whose inner product
        # with that of previous q point is 1
        #  e.g. < eig1(q=0) | eig1(q=1) >   = 1
        #       < eig1(q=0) | eig2(q=1) >   = 0

        index = []
        sort = []
        if i > 0:

            for x in xrange(len(evec_eq[i])):

                temp = []
                proj = []
                rel = []

                for y in xrange(len(evec_eq[i - 1])):
                    # Project, i.e. take the inner product of the two vectors
                    p = np.vdot(evec_eq[i][:, x].transpose(), evec_eq[i - 1][:, y])
                    proj.append(abs(p))
                    rel.append([x, y])

                for z in xrange(len(proj)):

                    if proj[z] == max(proj):
                        if len(index) < 6:
                            index.append([proj[z], rel[z][0], rel[z][1]])

        if i == 0:  # the first q point

            for j in xrange(len(evec_eq[i])):  # 3N; previously used dD instead of evec_eq but the dimensions should be the same

                gru.append([])
                gru_i.append([])
                omega_i.append([])

                evec_0 = np.asarray(evec_eq[i])  # 3N
                bra = evec_0[:, j]
                ket = evec_0[:, j].transpose()

                if dD.any():
                    d_eval = abs(np.vdot(bra, (np.dot(dD[i], ket) )))
                else:
                    d_eval = 0.0

                ##########################################
                ##   HERE WE CALCULATE GRUNEISEN PARAMETER
                ###################################################

                # throw away very low values of d_omega^2 because these won't contribute to
                # thermal conductivity and they will result in large, misleading Gruneisen parameters

                if abs(d_eval) < 1e-8:  # AND abs(eval_eq[i][j]) < ~ 0.3 THz
                    g = 0.0
                else:
                    if len(V) > 1:
                        g = - ( d_eval / (2 * eval_eq[i][j]) ) * ( V[0] / (V[1] - V[2]))

                gru[j + 1].append(float(g))
                gru_i[j + 1].append(j)
                omega_i[j+1].append(eval_eq[i][j])



            # Note: V elements MUST correspond to the correct calculations
            # V[0] = Veq ; V[1] = V+ ; V[2] = V-
            # I may want to change this later...


        else:  # all subsequent q points: need to use the index variable for sorting

            for j in xrange(len(eval_eq[i])):  # 3N (again using eval_eq instead of dD)

                #
                # We're going through the 3N items in the index
                #
                for x in xrange(len(index)):
                    #
                    # Check to see if the second number (i.e. the ket of the sorting projection)
                    # in the index is the mode we want to write a value to
                    #

                    if index[x][1] == j:

                        evec_q = np.asarray(evec_eq[i])

                        #try:
                        bra = evec_q[:, x]
                        ket = evec_q[:, x].transpose()
                        #except:
                        #    print index

                        '''NOTE: I changed this from dD to dD.any() on lines 177 and 128'''
                        if dD.any():
                            d_eval = abs(np.dot(bra, (np.dot(dD[i], ket) )))
                        else:
                            d_eval = 0.0

                        ## REJECT values where both eigenvalues are very small.
                        ## These are prone to error and have little physical meaning
                        ## NOTE: 2e-9 is somewhat arbitrary: it was the lowest value
                        #		I could assign where all of the Gru values stayed near
                        #		the peaks at gamma in PbTe

                        #d_eval is the eigenvalue (omega^2) for the non-equilibrium V
                        # eval_eq is the eigenvalue (omega^2) for the equilibrium V

                        if abs(d_eval) < 2e-9 and abs(eval_eq[i][j]) < 2e-9:
                            g = 0.0

                        else:
                            if len(V) > 1:
                                g = - ( d_eval / (2 * eval_eq[i][j]) ) * ( V[0] / (V[1] - V[2]))

                        gru[j + 1].append(float(g))
                        gru_i[j + 1].append(j)
                        omega_i[j+1].append(eval_eq[i][j])

                        # Get the acoustic modes
                        if round(eval_eq[i][j],10) == 0:
                            if('%s'%(BZ_path[i]) in acoustic.keys()):
                                acoustic['%s'%(BZ_path[i])].append(j)
                            else:
                                acoustic['%s'%(BZ_path[i])]=[j]



    return q, gru, gru_i, omega_i, acoustic

