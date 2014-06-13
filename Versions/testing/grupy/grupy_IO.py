import os
import json


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


## WRITE THE OUT FILE IN JSON FORMAT
def WriteGrupyFile ( Gout, Gin ):
	
	if Gin:
		gfile = "%s.grupy.bands.out" %Gout.prefix
	else:
		gfile = "%s.grupy.out" %Gout.prefix
	
	if os.path.isfile("%s" %(gfile) ):
		os.remove("%s" %(gfile)) #overwrite previous files
		
	#with open("%s.grupy.out"%Gout.prefix, "w") as file:
	with open('%s'%gfile, 'w') as file:
		
		## Write the high symmetry labels first
		for i in xrange( len(Gout.q_labels) ):
			label_line = {'prefix': '%s'%Gout.prefix,\
						  'label': '%s'%Gout.q_labels[i][0],\
						  'label_q': Gout.q_labels[i][1] } 
			l = json.dumps(label_line)
			file.write(l)
			file.write("\n")
	
	
	##Gout.gru_data[0] = list of q-points
	##Gout.gru_data[1 -> N] = list of Gruneisen parameters corresponding to those q-points
	
		## Now write the data

		if Gin:
			num = len(Gin.V)
		else:
			num = 1
		for X in range( num ):
		
			for j in xrange( len(Gout.gru_data[0])-1 ):  # q points
				
				if Gin:
					data_line = {'prefix': '%s'%Gout.prefix, \
								 'Calculation': '%s'%Gin.dir[X],\
								 'Volume':'%s'%Gin.V[X],  \
								 'q':'%s'%Gout.gru_data[X][j][0], 'Omega':[] }
				
					for i in xrange(1, len(Gout.gru_data[X][j]) ):
						data_line['Omega'].append('%s'%Gout.gru_data[X][j][i])
				
				
				else:	
					data_line = {'prefix': '%s'%Gout.prefix, \
								 'Volume': None, \
								'q':'%s'%Gout.gru_data[0][j], 'Gru':[] }
			
					for i in xrange(1, len(Gout.gru_data) ):  # modes
						data_line['Gru'].append('%s'%Gout.gru_data[i][j])

				l = json.dumps(data_line)
				file.write(l)
				file.write("\n")		
	

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