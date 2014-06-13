from qe.ReadDynMat import ReadDynMat
import numpy
import os


def GetBands ( Gin ):

	nat = Gin.nat
	amass = Gin.m
	dir = Gin.dir
	BZ_path = Gin.BZ_path

	bands = []
	
	q, Darray = ReadDynMat ( nat, amass, dir)
	
	for i in range( len (Darray) ):  # 3
	
		bands.append([])
		
		for j in xrange( len( Darray[i]) ):  # number of q points
			
			bands[i].append([])
			eval, evec = numpy.linalg.eigh( Darray[i][j] )
			#if j ==0:
				
				#print eval**0.5 * 3.289841973e3 #*33.35649629
				#print evec
			
			for k in xrange( len(eval)+1 ):  # 3N * 2 (because of the complex dynmat)
				
				if k == 0:
					bands[i][j].append( BZ_path[j] )
				
				else:	
				#these don't need to be sorted
					if eval[k-1] > 0:
						omega = (eval[k-1])**0.5 *3.289841973e3 #*33.35649629
					if eval[k-1] < 0:
						omega = ( -(-eval[k-1])**0.5 *3.289841973e3)# *33.35649629 )
					if eval[k-1] == 0:
						omega = 0	
					
					bands[i][j].append( omega )
					
	return bands
	
	
def WriteBands ( Gout, dir):
	
	gfile = "%s.grupy.bands.out" %Gout.prefix
	
	if os.path.isfile("%s" %(gfile) ):
		os.remove("%s" %(gfile)) #overwrite previous files
		
	file = open("%s.grupy.bands.out"%Gout.prefix, "w")
	
# PREFIX
	file.writelines("%s\n\n"%Gout.prefix)	
	
# HIGH SYMMETRY LABELS BLOCK
	
	file.writelines("LABELS\n\n")
		
	for i in xrange( len(Gout.q_labels) ):
			
		file.writelines("%s\t%s\n"%(Gout.q_labels[i][0], Gout.q_labels[i][1] ) )
			
	file.writelines("\n/END LABELS\n")


	print dir
# DATA BLOCK
	for i in range ( len(dir) ): #3

		file.writelines("\n%s DATA\n"%dir[i])
		
		for j in xrange( len(Gout.gru_data[i]) ): # number of q points
			
			cat = ""
			
			for k in xrange( len(Gout.gru_data[i][j]) ): # 3N +1
			
				cat = "%s\t%s"%(cat, Gout.gru_data[i][j][k] )
						
			file.writelines("%s\n"%cat)
			
		file.writelines("\n/END DATA\n\n")	
	
	file.close()
	
	return 0				