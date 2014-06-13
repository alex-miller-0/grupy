

def HighSymDatabase ( hs_points, sg, q):

	### Convert q vectors to strings (if no hs_points are provided):
	################################################################
	if not hs_points:
		qs = []
		
		for i in xrange(len(q)):
		
			temp = ""
			
			for j in xrange(len(q[i])):
			
				if j ==0:
			
					temp = "%s"%q[i][j].rstrip("0")
			
				if j >0:	
					
					temp = "%s, %s"%(temp, q[i][j].rstrip("0") )
				
			qs.append(temp)






	### Dictionaries:  (set up with trailing zeros stripped)
	########################################################
	
	sg225 = {'0., 0., 0.': 'G',
			 '0.5, 0., 0.5': 'X',
			 '0.5, 0.5, 0.5': 'L',
			 '0.5, 0.25, 0.75': 'W'}
			 
	
	
	
	

		
		
		
	
	### Check for high symmetry points:
	###################################
	highsym = []
	
	if hs_points:  # skip checking the database
	
		for i in range( len(q) ):
		
			for j in range( len(hs_points) ):
			
				if float(q[i][0]) == float(hs_points[j][1]):
					if float(q[i][1]) == float(hs_points[j][2]):
						if float(q[i][2]) == float(hs_points[j][3]):	
							
							highsym.append( [i, hs_points[j][0] ] )
	
		return highsym

	
	if str(sg) == "225":
		
		for i in range( len(qs) ):
			
			if qs[i] in sg225:
				
				highsym.append( [ i , sg225[ qs[i] ] ] )

	
	return highsym			