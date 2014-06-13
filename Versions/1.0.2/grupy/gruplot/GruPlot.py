# gets grupy data and runs a plotting function
import matplotlib.pyplot as plt

def GruPlot( prefix, labels, data):
	
	
	fig, axes = plt.subplots(nrows=1, ncols=1)
	x = []
	lab = []
	
	for i in xrange( len(labels) ):
		
		lab.append( labels[i][0] )
		x.append( float(labels[i][1]) )

	plt.xticks( x, lab)

	plt.title(prefix, fontsize=24)
	plt.ylabel(r"$\gamma$", fontsize=20, weight="bold")
	
		
	for i in xrange( len(data) ): # number of q points
			if i != 0:
				plt.plot( data[0] , data[i], 'o' )
	
	plt.show()	
		

	
	return 0

