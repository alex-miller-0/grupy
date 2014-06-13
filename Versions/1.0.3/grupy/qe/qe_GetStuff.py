import os
import sys


def GetPrefix ( directories ):
	
	prefix = []
	
	current_dir = os.getcwd()
	
	for x in directories:
		for file in os.listdir( "%s/%s/"%(current_dir, x) ):
			
			if file.endswith(".ph.out"):
		
				 prefix.append( file[ : len(file)-7] )	
	
	
	for x in xrange( len(prefix) ):
		
		if x > 0:
			
			if prefix[x] != prefix[x-1]:
				
				print "\n ATTENTION: 2 OR MORE PREFIXES DIFFER. THIS MAY RESULT IN ERROR."
				print " PLEASE DOUBLE CHECK YOUR CALCULATIONS\n"
		
						
	return prefix[0]
	

def GetNat_M_V ( dir, prefix ) :
	
	cwd = os.getcwd()  #current working directory
	nat = 0 #number of atoms
	V = [] #volumes (an array with dimension 1 x # calculations)
	m = [] # masses (an array with dimension 1 x nat)
	
	
	### prefix.dyn1 -- get nat and atomic masses	
	############################################
	
	for file in os.listdir( "%s/%s/"%(cwd, dir[0]) ):
		
		if file.endswith("%s.dyn1" %(prefix) ):
				
			temp_m = []  # for storing unique masses
			cwd = os.getcwd()
			
			name = "%s/%s/%s"%(cwd, dir[0] ,file)
			
			
			h = open('%s'%(name), 'rw')	
				
			num_atom_types = 0
				
			for i, line in enumerate(h):
				
				if i == 2:   # first get number of atoms and number of atom types
						
					temp = line.split()
					nat = int(temp[1])
					num_atom_types = int(temp[0])
					
				if i > 2:   # set a temporary array of unique masses
					
					for j in xrange( 1, num_atom_types+1 ):
							
						if "%s  \'"%(j) in line:
							temp = line.split()
							temp_m.append( temp[3] )
							
				if i > 2+num_atom_types:  # account for repeating atom types
					
					for j in xrange( 1, nat+1):
					
						for k in xrange( 1, num_atom_types+1):
								
							if "%s    %s"%(j,k) in line and len(line.split() )>2:
							
								temp = line.split()
								m.append( float( temp_m[ int(temp[1]) - 1 ] )   ) 
									# this will add masses in the correct order
									# as well as repeats if they arise
				
			h.close()				
						

		
		
	### prefix.out: get V (they are returned in the order that directories are given)
	#################################################################################
		
	cwd = os.getcwd()	
	for x in range( len(dir) ):
		
		for file in os.listdir( "%s/%s/"%(cwd, dir[x]) ):						
			
			if file.endswith("%s.out" %(prefix) ):
			
				cwd = os.getcwd()
				name = "%s/%s/%s"%(cwd, dir[x] ,file)
			
				f = open('%s'%(name), 'rw')	
			
				for line in f:
			
					if "unit-cell volume" in line:
				
						temp = line.split()
						V.append( float( temp[3] )  )   # these are only to 4 digits; not very accurate
			
				f.close()
			
		
			
				
	return nat, V , m
	
'''	
	
def GetMatdynModes( directories, nat):

	q = []
	omega = []
	modes= []
	

	current_dir = os.getcwd()
	
	for x in xrange( len(directories) ):
		
		modes.append([])
	
		
		for y in xrange( 3*int(nat) + 1):
			
			modes[x].append([])
		
		for file in os.listdir( "%s/%s/matdyn/"%(current_dir, directories[x]) ):
			
			if file.endswith("matdyn.modes" ):
				
				dir = os.getcwd()
				
				name = "%s/%s/matdyn/%s"%(current_dir, directories[x] ,file)
		
				f = open('%s'%(name), 'r')
				
				for line in f:
					
					if "q =" in line:
					
						temp = line.split()
						
						modes[x][0].append( [ temp[2], temp[3], temp[4] ]) # q
					
					elif "omega" in line:
						
						for i in xrange(1, len(modes[x])+1):
							
							
							if "omega( %s"%(i) in line:
						
								temp = line.split()
								
								modes[x][i].append( temp[6] ) #cm-1
								
								break
							
							elif "omega(%s"%(i) in line and len( str(i) ) > 1:
														
								temp = line.split()
								
								modes[x][i].append( temp[5] ) #cm-1
								
								break
							
	
	return modes		
				
	
def MakeQ2r (prefix, dirs):

	cwd = os.getcwd()
	
	for x in xrange( len(dirs) ):
		
		q2r = "%s/%s/q2r.in"%(cwd, dirs[x])
		
		if os.path.isfile("%s" %(q2r) ):
			os.remove("%s" %(q2r)) #overwrite previous files
		
			
		f = file("%s"%(q2r), "w")
		
		f.writelines('&input\n fildyn=\'%s.dyn\', flfrc=\'%s.fc\'/' %(prefix, prefix) )
	
		f.close()
	
	return 0	
	

	
def MakeMatdyn (dirs, prefix, path, m):

	cwd = os.getcwd()
	
	for x in xrange( len(dirs) ):
		matdyn = "%s/%s/matdyn.in"%(cwd, dirs[x])
		
		if os.path.isfile("%s" %(matdyn) ):
			os.remove("%s" %(matdyn)) #overwrite previous files
			
		f = file("%s"%(matdyn), "w")
		
		f.writelines("&input\n") #start input block
			
		for i in xrange( len(m) ):
			
			m[i] /= (1.660538782E-27/(2*9.10938215E-31))  #converting from espresso units
			f.writelines("amass(%s)= %s,\n"%(i+1, m[i]) ) #write masses in correct format
			
		f.writelines ("flfrc=\'%s.fc\', flfrq=\'%s.freq\' " %(prefix, prefix) )
		f.writelines("fldyn=\'%s.dynmat\' " %(prefix) )
		f.writelines("\n/\n")
	
		f.writelines( "%s\n"%( len(path) ) )


		#write the path	
		for i in xrange( len(path) ):
				
			for j in xrange( len(path[i]) ):
					
				f.writelines( "%s\t"%(path[i][j]) )
			
			f.writelines("\n")			

		f.close()	
	
	return 0
	




def MakePath ( path  ):

	
	to_return = []
	
	for i in xrange( len(path) ):
		
		if i > 0:
		
			dist1 = ( float(path[i][0]) - float(path[i-1][0]))
			dist2 = ( float(path[i][1]) - float(path[i-1][1]))
			dist3 = ( float(path[i][2]) - float(path[i-1][2]))		
			
			for x in xrange(101):
			
				p=[(path[i-1][0] + x*(dist1/100)) , (path[i-1][1]+ x*(dist2/100)), (path[i-1][2] + x*(dist3/100)) ]
				
				to_return.append( [ round(p[0],3), round(p[1],3), round(p[2],3) ] )
	
	return to_return	
			
				
'''	
	