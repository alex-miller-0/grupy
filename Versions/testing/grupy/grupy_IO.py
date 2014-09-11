import os
import json





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

            #for j in xrange(len(Gout.gru_data[0]) - 1):  # q points

            for j in xrange(len(Gout.phonons[X]) - 1):

                ### FOR PHONON BANDS DISPERSIONS
                if bands_true == 1:

                    #if len(Gout.gru_data[X][j]) > 1:
                        #for i in xrange(1, len(Gout.phonons[X][j])):  # 3N modes
                        for i in xrange(3*Gin.nat):
                            data_line = {'prefix': Gout.prefix,
                                         'calculation': Gout.calc[X],
                                         'volume': Gout.V[X],
                                         'q': Gout.phonons[X][j]['cartQ'],
                                         'reducedPath': Gout.phonons[X][j]['reducedQ'],
                                         'mode': i+1,
                                         'omega': Gout.phonons[X][j]['%s'%(i+1)]

                            }

                            data_line['modeType'] = "O"
                            if data_line['mode'] in Gout.acoustic[X]:
                                data_line['modeType'] = "A"



                            l = json.dumps(data_line)
                            file.write(l)
                            file.write("\n")


                ### FOR GRUNEISEN PARAMETER
                else:

                    for i in xrange(3*Gin.nat):  # 3N modes

                        data_line = {'prefix': Gout.prefix,
                                     'calculation': Gout.calc[X],
                                     'volume': Gout.V[X],
                                     'q': Gout.gruneisen[j]['cartQ'],
                                     'reducedPath': Gout.gruneisen[j]['reducedQ'],
                                     'mode': i+1,
                                     'Gruneisen': Gout.gruneisen[j]['Gruneisen']['%s'%(i+1)]

                        }

                        data_line['modeType'] = "O"
                        if data_line['mode'] in Gout.acoustic[X]:
                            data_line['modeType'] = "A"


                        if not Gin.path:
                            data_line['Omega_eq']= '%s' %Gout.omega_eq[j][i]
                        l = json.dumps(data_line)
                        file.write(l)
                        file.write("\n")



    return 0
