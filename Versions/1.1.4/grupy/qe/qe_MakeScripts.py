import os


def MakeQ2r(prefix, dirs):
    cwd = os.getcwd()

    for x in xrange(len(dirs)):

        q2r = "%s/%s/q2r.in" % (cwd, dirs[x])

        if os.path.isfile("%s" % (q2r)):
            os.remove("%s" % (q2r))  # overwrite previous files

        f = file("%s" % (q2r), "w")

        f.writelines('&input\n fildyn=\'%s.dyn\', flfrc=\'%s.fc\', zasr=\'crystal\'/' % (prefix, prefix))

        f.close()

    return 0


def MakeMatdyn(dirs, prefix, path, m):
    for i in xrange(len(m)):
        m[i] /= (1.660538782E-27 / (2 * 9.10938215E-31))  # converting from espresso units

    cwd = os.getcwd()

    for x in xrange(len(dirs)):
        matdyn = "%s/%s/matdyn.in" % (cwd, dirs[x])

        if os.path.isfile("%s" % (matdyn)):
            os.remove("%s" % (matdyn))  # overwrite previous files

        f = file("%s" % (matdyn), "w")

        f.writelines("&input\n")  # start input block

        for i in xrange(len(m)):
            f.writelines("amass(%s)= %sd0,\n" % (i + 1, m[i]))  # write masses in correct format

        f.writelines("flfrc=\'%s.fc\', flfrq=\'%s.freq\', asr=\'crystal\' " % (prefix, prefix))

        if path:
            f.writelines("fldyn=\'%s.dynmat\' " % (prefix))

        if not path:
            f.writelines("dos=.true., nk1=10, nk2=10, nk3=10, deltaE=5 ")



        f.writelines("\n/\n")


        if path:
            f.writelines("%s\n" % ( len(path) ))


            # write the path
            for i in xrange(len(path)):

                for j in xrange(len(path[i])):
                    f.writelines("%s\t" % (path[i][j]))

                f.writelines("\n")

            f.close()

    return 0