# gets grupy data and runs a plotting function
import matplotlib.pyplot as plt
import numpy

def GruPlot( prefix, labels, data, type):
	
	
	fig, axes = plt.subplots(nrows=1, ncols=1)
	x = []
	lab = []
	
	for i in xrange( len(labels) ):
		
		lab.append( labels[i]['label'] )
		x.append( float(labels[i]['label_q']) )
		plt.axvline(x=float(labels[i]['label_q']) , color='black')
		
	plt.xticks( x, lab)

	plt.title(prefix, fontsize=22)
	
	if type == 'bands':
		plt.ylabel(r"$Mode$ $\omega$ $(THz)$", fontsize=20, weight="bold")
	else:
		plt.ylabel(r"$Gr\ddotuneisen$ $\gamma$", fontsize=20, weight="bold")
	
	
	
	data = numpy.asarray(data)
	
	if type == 'bands':
		for i in range( len(data[0]) ): # number of modes
			if i!=0:
				plt.plot ( data[:,0], data[:,i], '-')
	
	else:
		for i in range( len(data[0]) ): # number of modes
			if i!=0:
				plt.plot ( data[:,0], data[:,i], '.')
	
	
	plt.show()	
		

	
	return 0

