import numpy as np
import os
from decimal import *


# CREATES AN ARRAY OF NUMPY ARRAYS, EACH CONTAINING A DYNAMICAL MATRIX READ FROM THE FILE

#	FIRST, AN ARRAY OF REGULAR ARRAYS WILL BE CREATED
#	NEXT, THESE ARRAYS WILL BE CONVERTED TO NUMPY ARRAYS AND REPACKAGED IN
#		A NEW, REGULAR ARRAY


def ReadDynMat(nat, amass, dir):
    # Note: QE produces atomic masses in a weird unit
    # They are first extracted from prefix.dyn1



    D = []  # dynamical matrix

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
        D.append([])

        for file in os.listdir("%s/%s/" % (cwd, dir[x])):

            if file.endswith(".dynmat"):

                name = "%s/%s/%s" % (cwd, dir[x], file)

                f = open(name, 'r')

                for i, line in enumerate(f):

                    if "q" in line and "=" in line:

                        qcount += 1
                        start = i + 2
                        end = i + 2 + (4 * nat * nat)

                        D[x].append([])

                        temp = line.split()

                        q.append([temp[3], temp[4], temp[5]])



                    if start <= i and i <= end and start != 0 and end != 0:

                        if len(line.split()) == 2:

                            m1 = amass[-1 + int(line.split()[0])]
                            m2 = amass[-1 + int(line.split()[1])]
                            row = int(line.split()[0]) - 1
                            col = int(line.split()[1]) - 1
                            incount = i

                            if int(line.split()[0]) == 1:
                                D[x][qcount - 1].append([])
                                D[x][qcount - 1].append([])
                                D[x][qcount - 1].append([])

                        if len(line.split()) == 6:

                            temp = line.split()
                            M = (m1 * m2) ** 0.5

                            if i == incount + 1:
                                a = (float(temp[0]) + 1j * float(temp[1]) ) / M
                                b = (float(temp[2]) + 1j * float(temp[3]) ) / M
                                c = (float(temp[4]) + 1j * float(temp[5]) ) / M

                                D[x][qcount - 1][(3 * col)].append(a)
                                D[x][qcount - 1][(3 * col)].append(b)
                                D[x][qcount - 1][(3 * col)].append(c)  #Throwing out imaginary columns
                                # (They should be 0 anyway)
                            if i == incount + 2:
                                a = (float(temp[0]) + 1j * float(temp[1]) ) / M
                                b = (float(temp[2]) + 1j * float(temp[3]) ) / M
                                c = (float(temp[4]) + 1j * float(temp[5]) ) / M

                                D[x][qcount - 1][1 + (3 * col)].append(a)
                                D[x][qcount - 1][1 + (3 * col)].append(b)
                                D[x][qcount - 1][1 + (3 * col)].append(c)

                            if i == incount + 3:
                                a = (float(temp[0]) + 1j * float(temp[1]) ) / M
                                b = (float(temp[2]) + 1j * float(temp[3]) ) / M
                                c = (float(temp[4]) + 1j * float(temp[5]) ) / M

                                D[x][qcount - 1][2 + (3 * col)].append(a)
                                D[x][qcount - 1][2 + (3 * col)].append(b)
                                D[x][qcount - 1][2 + (3 * col)].append(c)

                f.close()
    D = np.asarray(D)

    return q, D
