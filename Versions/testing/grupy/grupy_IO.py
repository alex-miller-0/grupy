import os
import json


def GetInput():
    dir = []
    # sg = ""
    bz_path = []
    temps = []

    cwd = os.getcwd()

    for file in os.listdir(cwd):
        if file.lower() == "grupy.in":
            f = open(file, 'r')

            for line in f:
                if "dir" in line.lower():
                    s = line.split()
                    for i in xrange(len(s)):
                        if i > 0 and s[i] != "=":
                            dir.append(s[i])

                if "path" in line.lower():
                    s = line.split()
                    if (len(s) - 1) % 4 != 0:
                        print "Error: check your BZ path and make sure all points are labelled"
                        return 0
                    n = ((len(s) - 1) / 4)

                    for i in xrange(0, n):
                        label = s[1 + i * 4]
                        one = float(s[2 + i * 4])
                        two = float(s[3 + i * 4])
                        three = float(s[4 + i * 4])

                        c = [label, one, two, three]

                        bz_path.append(c)
                if "temps" in line.lower():
                    s = line.split()
                    for i in range(len(s)):
                        try:
                            t = float(s[i])
                            temps.append(t)
                        except:
                            pass





            f.close()

    return dir, bz_path, temps


# # WRITE THE OUT FILE IN JSON FORMAT
def WriteGrupyFile(Gout, Gin, bands_true):


    if bands_true == 1:
        gfile = "%s.grupy.bands.out" % Gout.prefix
    else:
        gfile = "%s.grupy.out" % Gout.prefix

    if os.path.isfile("%s" % (gfile)):
        os.remove("%s" % (gfile))  # this will overwrite previous files

    #with open("%s.grupy.out"%Gout.prefix, "w") as file:
    with open('%s' % gfile, 'w') as file:
        l = json.dumps({"units":'%s'%(Gout.units)})
        file.write("%s\n"%l)
        if Gin.path:
            ## Write the high symmetry labels first
            for i in xrange(len(Gout.q_labels)):
                label_line = {'prefix': '%s' % Gout.prefix,
                              'num_modes': '%s' % (3 * Gin.nat),
                              'label': '%s' % Gout.q_labels[i][0],
                              'label_q': Gout.q_labels[i][1]}
                l = json.dumps(label_line)
                file.write(l)
                file.write("\n")

        ## Now write the data

        if bands_true == 1:
            num = len(Gin.V)
        else:
            num = 1


        for X in range(num):  # number of calculations (i.e. 3 for bands, 1 for Gru)

            for j in xrange(len(Gout.gru_data[0]) - 1):  # q points

                ### FOR PHONON BANDS DISPERSIONS
                if bands_true == 1:

                    if len(Gout.gru_data[X][j]) > 1:
                        for i in xrange(1, len(Gout.gru_data[X][j])):  # 3N modes


                            data_line = {'prefix': '%s' % Gout.prefix,
                                         'Calculation': '%s' % Gin.dir[X],
                                         'Volume': '%s' % Gin.V[X],
                                         'q': '%s' % Gout.gru_data[X][j][0],
                                         'Mode_Index': '%s' % Gout.mode_index[i][j],
                                         'Omega': '%s' % Gout.gru_data[X][j][i],
                                         'Group_Velocity': '%s' % Gout.group_velocity[X][j][i]

                                        }

                            data_line['Mode_Type'] = "O"
                            for k in range(len(Gout.acoustic_i)):
                                if int(Gout.acoustic_i[k]) == int(Gout.mode_index[i][j]):
                                    data_line['Mode_Type'] = "A"
                                    break

                            l = json.dumps(data_line)
                            file.write(l)
                            file.write("\n")

                            #for i in xrange(1, len(Gout.gru_data[X][j]) ):
                        #	data_line['Omega'].append('%s'%Gout.gru_data[X][j][i])
                        #	data_line['Mode_Index'].append('%s'%Gout.mode_index[X][j][i])


                    # else you may just want to generate data for/plot a single band structure
                    else:

                        data_line = {'prefix': '%s' % Gout.prefix,
                                     'Calculation': '%s' % Gin.dir[X],
                                     'Volume': '%s' % Gin.V[X],
                                     'q': '%s' % Gout.gru_data[X][j][0],
                                     'Mode_Index': '%s' % Gout.mode_index[i][j],
                                     'Omega': '%s' % Gout.gru_data[X][j][i],
                                     'Group_Velocity': '%s' % Gout.group_velocity[X][j][i]
                                    }

                        data_line['Mode_Type'] = "O"
                        for k in range(len(Gout.acoustic_i)):
                            if int(Gout.acoustic_i[k]) == int(Gout.mode_index[i][j]):
                                data_line['Mode_Type'] = "A"
                                break

                        l = json.dumps(data_line)
                        file.write(l)
                        file.write("\n")

                ### FOR GRUNEISEN PARAMETER
                else:
                    #print num
                    #print Gout.omega_eq
                    for i in xrange(1, len(Gout.gru_data)):  # 3N modes

                        data_line = {'prefix': '%s' % Gout.prefix,
                                     'Volume': None,
                                     'q': '%s' % Gout.gru_data[0][j],
                                     'Mode_Index': '%s' % Gout.mode_index[i][j],
                                     'Gru': '%s' % Gout.gru_data[i][j],
                                    }

                        data_line['Mode_Type'] = "O"
                        for k in range(len(Gout.acoustic_i)):
                            if int(Gout.acoustic_i[k]) == int(Gout.mode_index[i][j]):
                                data_line['Mode_Type'] = "A"
                                break

                        if not Gin.path:
                            data_line['Omega_eq']= '%s' %Gout.omega_eq[j][i]
                        l = json.dumps(data_line)
                        file.write(l)
                        file.write("\n")

                        #for i in xrange(1, len(Gout.gru_data) ):  # 3N modes
                    #	data_line['Gru'].append('%s'%Gout.gru_data[i][j])
                    #	data_line['Mode_Index'].append('%s'%Gout.mode_index[i][j])

                    #l = json.dumps(data_line)
                    #file.write(l)
                    #file.write("\n")


    return 0
