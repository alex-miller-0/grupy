# gets grupy data and runs a plotting function
import matplotlib.pyplot as plt
import numpy

def GruPlot( prefix, labels, data):
	
	fig, axes = plt.subplots(nrows=1, ncols=1)
	x = []
	lab = []
	
	for i in xrange( len(labels) ):
		
		lab.append( labels[i]['label'] )
		x.append( float(labels[i]['label_q']) )

	plt.xticks( x, lab)

	plt.title(prefix, fontsize=24)
	plt.ylabel(r"$\gamma$", fontsize=20, weight="bold")
	
	data = numpy.asarray(data)
	#for i in xrange( len(data) ): # number of q points
	#		if i != 0:
	#			plt.plot( data[i][0] , data[i][1:], 'o' )
	
	for i in range( len(data[0]) ): # number of modes
		if i!=0:
			plt.plot ( data[:,0], data[:,i], 'o')
	
	plt.show()	
		

	
	return 0

