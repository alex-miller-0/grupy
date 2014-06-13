# gets grupy data and runs a plotting function
import matplotlib.pyplot as plt

def GruPlot( prefix, q_labels, gru_data):

	fig, axes = plt.subplots(nrows=1, ncols=1)
	x = []
	lab = []
	
	for i in xrange( len(q_labels) ):
		lab.append( q_labels[i][1] )
		x.append( q_labels[i][0] )
	
	plt.setp(axes, xticks=x, xticklabels=lab)
	plt.title(prefix, fontsize=24)
	plt.ylabel(r"$\gamma$", fontsize=20, weight="bold")
	
		
	for i in xrange( len(gru_data) ): # 3N columns
		
		if i != 0:
			plt.plot( gru_data[0] , gru_data[i], 'o' )
	
	plt.show()	
				

	
	return 0

