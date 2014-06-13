import os

def RunQ2r ( dir ):

	cwd = os.getcwd() 

	for i in xrange( len(dir) ):
		
		os.system( "q2r.x < %s/%s/q2r.in" %(cwd, dir[i]  )
	
	return 0
	
	
	
def RunMatdyn ( dir ):

	cwd = os.getcwd()
	
	for i in xrange( len(dir) ):
		
		os.system( "matdyn.x < %s/%s/matdyn.in" %(cwd, dir[i] )
	
	return 0