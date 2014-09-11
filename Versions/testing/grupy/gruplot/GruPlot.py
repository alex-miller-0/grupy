# gets grupy data and runs a plotting function
import matplotlib.pyplot as plt
import numpy


def GruPlot(prefix, num_modes, labels, q, data, mode_i, type, units):
    fig, axes = plt.subplots(nrows=1, ncols=1)
    x = []
    lab = []
    y_data = []
    q_data = []

    for i in xrange(len(labels)):
        lab.append(labels[i]['label'])
        x.append(float(labels[i]['label_q']))
        plt.axvline(x=float(labels[i]['label_q']), color='black')

    plt.xticks(x, lab)

    plt.title(prefix, fontsize=22)



    if type == 'bands':
        if units=="thz":
            plt.ylabel(r"$Mode$ $\omega$ $(THz)$", fontsize=20, weight="bold")
        elif units=="cm-1":
            plt.ylabel(r"$Mode$ $\omega$ $(cm^{-1})$", fontsize=20, weight="bold")
    else:
        plt.ylabel(r"$Gr\ddotuneisen$ $\gamma$", fontsize=20, weight="bold")

    data = numpy.asarray(data)

    # if type == 'bands':
    #	for i in range( len(data[0]) ): # number of modes
    #		if i!=0:
    #			plt.plot ( data[:,0], data[:,i], '-')


    #for i in range( len(data[0]) ): # number of modes
    #	if i!=0:
    #		plt.plot ( data[:,0], data[:,i], '.')

    for j in xrange(num_modes):
        y_data.append([])
        for i in xrange(len(data)): # should be equal to length of q and mode_i
            if int(mode_i[i]) == j+1:

                # make 3N (i.e. number of modes) sets of y_data
                y_data[j].append(data[i])

                # only make the q_data values once (they are used by every mode)
                if mode_i[i] == 1:
                    q_data.append(q[i])




    ## NOW PLOT
    if type == 'bands':
        for k in xrange(num_modes):
            plt.plot(q_data, y_data[k], '-')
    else:
        for k in xrange(num_modes):
            plt.plot(q_data, y_data[k], '.')

    plt.grid()




    plt.show()

    return 0

