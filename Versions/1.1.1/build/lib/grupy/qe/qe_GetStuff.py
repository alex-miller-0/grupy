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
