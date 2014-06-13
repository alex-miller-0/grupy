##diagonalize
import numpy as np
from qe.ReadDynMat import *
import cmath





def Get_Eval_Evec_dDdV ( Darray):
	

	
	Deq = []   ## equilibrium dyn matrices
	Dn = []		## non-equilibrium dyn matrices
	dD = []   ## what will be returned (dD/dV)
	eval = []	## eigenvalues (omega^2) 
	evec = []	## eigenvectors that diagonalize eq matrices
	
	
	for x in xrange( len(Darray) ):  ## for each calculation there will be a subarray
		
		if x != 0:  ## i.e. not an equilibrium matrix
		
			Dn.append([])
		
		for y in xrange( len(Darray[x]) ): ## for each q point there will be a subarray
		
			if x == 0:  ## i.e. if we are looking at the equilibrium matrices
				
				#evec.append([])
				eval.append([])
				
				Deq.append ( Darray[0][y] )  ## the format needs to be that the EQUILIBRIUM dimension 
							 				 ## is imported FIRST
		
				evali, eveci = np.linalg.eigh(Darray[0][y])
				
				
				eveci = np.asarray( eveci )
				
				for z in xrange( len(evali) ):
					eval[y].append( evali[z] )  ## populate eigenvalues
				
				# before i had evec[y].append but i think that gives wrong dimensions
				evec.append( eveci ) ## populate eigenvectors (3N x 3N matrix)
				
				  
			else:  ## i.e. non-equilibrium matrices

				Dn[x-1].append(Darray[x][y])  ## this is a full dyn matrix

	
	# Dn array should have 2 columns of elements (for + and - volume calculations)
	#	, with each element being a 3Nx3N matrix of eigenvalues at that q-point
	# Deq array should have three dimensions	
	
	
	for i in xrange(len(Deq)):  # q points
		
		dD.append([])
		
		for j in xrange( len(Deq[i]) ):  # 3N
			
			dD[i].append([])
			
			for k in xrange( len(Deq[i][j]) ):  # 3N
			
				dD[i][j].append( (Dn[0][i][j][k] - Dn[1][i][j][k]) )
				# Dn[0] is D+ , Dn[1] is D-
	
	
	
	return eval, evec, dD
	
		


## Calculate Gruneisen parameter

def GruCalc ( V, nat, amass, dir ):

	q, Darray = ReadDynMat ( nat, amass, dir)  # get dynamical matrices (eq, +, and -)
	
	eval_eq, evec_eq, dD = Get_Eval_Evec_dDdV ( Darray)  # get equilibrium eigenvalues
												   # and eigenvectors as well as the
												   # dD matrix
	
	gru = []
	gru.append([]) # for the q point column
	
	
	for i in xrange( len(dD) ):  ## should be equal to the number of q points
		gru[0].append(i+1) # append q point number (not the actual q point)
		
		
		
		# SORTING of eigenvalues: must correspond to eigenvectors whose inner product
		# with that of previous q point is 1
		#  e.g. < eig1(q=0) | eig1(q=1) >   = 1
		#       < eig1(q=0) | eig2(q=1) >   = 0
		
		index = []
		if i > 0:
	
			for x in xrange( len(evec_eq[i]) ):
				
				temp = []
	
				for y in xrange( len(evec_eq[i-1]) ):
					
					# Project, i.e. take the inner product of the two vectors
					proj = np.dot( evec_eq[i][:,x].transpose() , evec_eq[i-1][:,y] )
					temp.append( [abs(proj) , x, y] )	
					
				index.append( max(temp)  ) # Take the max; should be close to 0
		
		########
		
		
		
		if i == 0:  # the first q point
		
			for j in xrange( len(dD[i]) ):  ## 3N

				gru.append([])

				evec_0 = np.asarray( evec_eq[i] )  # 3Nx3N matrix
	
				bra = evec_0[:,j]
				ket = evec_0[:,j].transpose()
		
				d_eval = np.dot( bra, (np.dot(dD[i] , ket) ) ).real
			
			# throw away very low values of d_omega^2 because these won't contribute to 
			# thermal conductivity and they will result in large, misleading Gruneisen parameters
			
				if abs(d_eval) < 1e-8:  # AND abs(eval_eq[i][j]) < ~ 0.3 THz
					g = 0.0
			
				else:
					g = - ( d_eval/(2*eval_eq[i][j]) )* ( V[0]/(V[1]-V[2]))

				gru[j+1].append( float(g) )
			
			# Note: V elements MUST correspond to the correct calculations
			# V[0] = Veq ; V[1] = V+ ; V[2] = V-
			# I may want to change this later...
			
			
		else: # all subsequent q points: need to use the index variable for sorting
			for j in xrange( len(dD[i]) ): # 3N
				
				
				for x in xrange( len(index) ):
					if index[x][2] == j:
						
						evec_q = np.asarray( evec_eq[i])
						bra = evec_q[:,x]
						ket = evec_q[:,x].transpose()
						
						d_eval = np.dot( bra, (np.dot(dD[i] , ket) ) ).real
						
						if abs(d_eval) < 1e-8 and abs(eval_eq[i][j]) < 1e-7:
							g = 0.0
			
						else:
							g = - ( d_eval/(2*eval_eq[i][j]) )* ( V[0]/(V[1]-V[2]))
	
						gru[j+1].append( float(g) )
					
					
	
	return q, gru		
	
	
''' ARCHIVE

def Get_Eval_Evec_dDdV ( Darray, V):
	
	# MAY NOT NEED TO CONVERT UNITS
	# convert Volume:  Bohr^3 to A^3
	#for i in range(len(V)):
	#	V[i] *=  (0.52917720859e-10)**3
	
	Deq = []   ## equilibrium dyn matrices
	Dn = []		## non-equilibrium dyn matrices
	dDdV = []   ## what will be returned (dD/dV)
	delDdelV = []  ## the average of dDdV, this one will be returned
	eval = []	## eigenvalues (omega^2) 
	evec = []	## eigenvectors that diagonalize eq matrices
	
	
	for x in xrange( len(Darray) ):  ## for each calculation there will be a subarray
		
		if x != 0:  ## i.e. not an equilibrium matrix
		
			Dn.append([])
		
		for y in xrange( len(Darray[x]) ): ## for each q point there will be a subarray
		
			if x == 0:  ## i.e. if we are looking at the equilibrium matrices
				
				evec.append([])
				eval.append([])
				
				Deq.append ( Darray[0][y] )  ## the format needs to be that the EQUILIBRIUM dimension 
							 				 ## is imported FIRST
		
				evali, eveci = np.linalg.eig(Darray[0][y])
				
				
				eveci = np.asarray( eveci )
				
				for z in xrange( len(evali) ):
					eval[y].append( evali[z] )  ## populate eigenvalues
				
				evec[y].append( eveci ) ## populate eigenvectors (3N x 3N matrix)
				
				  
			else:  ## i.e. non-equilibrium matrices

				Dn[x-1].append(Darray[x][y])  ## this is a full dyn matrix

		
	# Dn array should have four dimensions,
	# Deq array should have three dimensions	
		
	for x in xrange( len(Dn) ):	# dimensions including NON-equilibrium calculations
		
		dDdV.append([])

		
		for i in xrange( len(Deq) ):
			
			dDdV[x].append([])
			
			if x==0:
				delDdelV.append([])
			
			for j in xrange( len(Deq[i]) ):
				
				dDdV[x][i].append([])
				
				if x==0:
					delDdelV[i].append([])
				
				for k in xrange( len(Deq[i][j]) ):  ## populate dD/dV matrix values
					
					dDdV[x][i][j].append( (Dn[x][i][j][k] - Deq[i][j][k])/( V[x+1]-V[0] ) )
					
					if x==0:
						delDdelV[i][j].append(0.0)
					
					
		

	for x in xrange( len(dDdV) ):
	
		for i in xrange( len(delDdelV) ):
			
			for j in xrange( len(delDdelV[i]) ):
			
				for k in xrange( len(delDdelV[i][j]) ):
				
					delDdelV[i][j][k] += dDdV[x][i][j][k]
					
					if x == len(dDdV)-1:
						
						delDdelV[i][j][k] /= (x+1) 
					
			
	return eval, evec, delDdelV
	
	
def GruCalc ( V, nat, amass, dir ):

	Darray = ReadDynMat ( nat, amass, dir)
	
	eval, evec, dD = Get_Eval_Evec_dDdV ( Darray)
	
	gru = []
	gru.append([]) # for q point column
	
	
	
	
	for i in xrange( len(dD) ):  ## should be equal to the number of q points
		gru[0].append(i+1)
		
		
		for j in xrange( len(dD[i]) ):  ## 3N
			
			if i==0:  # happens 3N times
				gru.append([])
	
		
			eigvec = np.asarray( evec[i] )
				
			bra = eigvec[:,j]
			ket = eigvec[:,j].transpose()
		
			d_eval = np.dot( bra, (np.dot(dD[i] , ket) ) ).real
			
			
			# Note: V elements MUST correspond to the correct calculations
			# V[0] = Veq ; V[1] = V+ ; V[2] = V-
			
			
			# throw away very low values of d_omega^2 because these won't contribute to 
			# thermal conductivity and they will result in large, misleading Gruneisen parameters
			if abs(d_eval) < 1e-8:
				g = 0.0
			
				
			else:
				g = - ( d_eval/(2*eval[i][j]) )* ( V[0]/(V[1]-V[2]))
				
			
			
			gru[j+1].append( float(g) )
			
		
	return gru		
'''			
