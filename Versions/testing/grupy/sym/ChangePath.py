import numpy as np

def ConvertPath ( Gin ):
	old_path = Gin.path
	old_basis = Gin.basis
	sg = Gin.sg
	new_path = []
#	
#	Tensor relating old_basis to new_basis 	
#
	tensor = ChangeBasis( old_basis, sg)
	
	for i in xrange( len(old_path) ):
	
		new_path.append( [np.dot( old_path[i], tensor)] 