import os


def GetInput():
	dir = []
	sg = ""
	bz_path = []
	
	cwd = os.getcwd()
	
	for file in os.listdir( cwd ) :
	
		if file.lower() == "grupy.in":
			
			f = open(file, 'r')
			
			for line in f:
				
				if "dir" in line.lower():
				
					s = line.split()
					
					for i in xrange( len( s )):
					
						if i>0 and s[i] != "=":
							
							dir.append( s[i] )
				
				if "space_group" in line.lower():
				
					s = line.split()
					
					for i in xrange( len( s )):
					
						if i>0 and s[i] != "=":
						
							sg = s[i]	
				'''			
				if "path" in line.lower():
				
					s = line.split()
					
					if (len(s)-1)%3 != 0:
						print "Error: check your BZ path"
						return 0
						
					n = ((len(s)-1)/3)
					
					
					for i in xrange( 0, n ):
						
						one = float( s[1 + i*3] )
						two = float( s[2 + i*3] )
						three = float( s[3 + i*3] )
						
						c = [ one, two, three]
						hs_path.append(c)
				'''	
				if "path" in line.lower():
				
					s = line.split()
					
					if (len(s)-1)%4 != 0:
						print "Error: check your BZ path and make sure all points are labelled"
						return 0
						
					n = ((len(s)-1)/4)
					
					
					for i in xrange( 0, n ):
						
						
						label = s[ 1+ i*4]
						one = float( s[2 + i*4] )
						two = float( s[3 + i*4] )
						three = float( s[4 + i*4] )
						
						c = [ label, one, two, three]
						
						bz_path.append(c)
				
		
				
								
			f.close()
	'''
	if not dirs or sg == "" or not path:
		print "Error: input file is missing something...\n"
		print "DIRS = directories of calculations\n"
		print "SPACE_GROUP = space group of structure\n"
		print "PATH = BZ path, i.e. 0 0 0   0.5 0.5 0.5"
		return 0
	'''
	return dir, sg, bz_path


def WriteGrupyFile ( Gout ):
	
	gfile = "%s.grupy.out" %Gout.prefix
	
	if os.path.isfile("%s" %(gfile) ):
		os.remove("%s" %(gfile)) #overwrite previous files
		
	file = open("%s.grupy.out"%Gout.prefix, "w")
	
	# PREFIX
	file.writelines("%s\n\n"%Gout.prefix)	
	
	
	# HIGH SYMMETRY LABELS BLOCK
	
	file.writelines("LABELS\n\n")
		
	for i in xrange( len(Gout.q_labels) ):
			
		file.writelines("%s\t%s\n"%(Gout.q_labels[i][0], Gout.q_labels[i][1] ) )
			
	file.writelines("\n/END LABELS\n")

	
	# DATA BLOCK	
	file.writelines("\nDATA\n")
		
	for j in xrange( len(Gout.gru_data[0])-1 ):
		
		cat = ""
			
		for i in xrange( len(Gout.gru_data) ):
			
			cat = "%s\t%s"%(cat, Gout.gru_data[i][j] )
					
		file.writelines("%s\n"%cat)
			
	file.writelines("\n/END DATA")	
	
	file.close()
	
	return 0
	
'''	
def ReadGrupyFile( ):
	
	cwd = os.getcwd()
	
	for file in os.listdir( "%s/"%(cwd) ):
		
		if file.endswith("%s.grupy.out"%prefix):
		
			f = open('%s/%s.grupy.out'%(cwd,prefix), 'rw')
			
			for i, line in enumerate(f):
			
				if 			
			
			
			f.close()
		
'''	