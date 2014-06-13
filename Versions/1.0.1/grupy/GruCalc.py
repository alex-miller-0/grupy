##diagonalize
import numpy as np
from qe.ReadDynMat import *
import cmath


def Get_Eval_Evec_dDdV  ( Darray , BZ_path ):
	
	#Deq = []   ## equilibrium dyn matrices
	Dn = []		## non-equilibrium dyn matrices
	dD = []   ## what will be returned (dD/dV)
	EVAL = []	## eigenvalues (omega^2) 
	EVEC = []	## eigenvectors that diagonalize eq matrices

	

	
	for i in range( len (Darray) ):  # 3
		
		if i != 0:  ## i.e. not an equilibrium matrix
		
			Dn.append([])

		
		for j in xrange( len( Darray[i]) ):  # number of q points
		
			
					
			if i == 0: ## again, just looking at equilibrium matrices
				
				EVAL.append( [] )
				EVEC.append( [] )
			
				eval, evec = np.linalg.eigh( Darray[i][j] )

				#Deq.append ( Darray[0][j] )
				
				for k in xrange( len(eval) ):  # 3N * 2 (because of the complex dynmat)
					# TESTING: should be 3N now
					EVAL[j].append(eval[k])
					EVEC[j].append(evec[k])
					#if k != 0:
					
					#	EVEC[j].append( evec[k-1] ) 
					
					#	if k%2 == 0:  # half of the eigenvalues will be duplicates
					#		EVAL[j].append( eval[k-1] )
					
			
			else: ## i.e. NON-equilibrium matrices
				Dn[i-1].append(Darray[i][j])  ## this is a full dyn matrix
				
	
	# Dn array should have 2 columns of elements (for + and - volume calculations)
	#	, with each element being a 3Nx3N matrix of eigenvalues at that q-point
	# Deq array should have three dimensions	
	
	
	for i in xrange(len(Darray[0])):  # q points
		
		dD.append([])
		
		for j in xrange( len(Darray[0][i]) ):  # 3N * 2
			
			dD[i].append([])
			
			for k in xrange( len(Darray[0][i][j]) ):  # 3N*2
			
				dD[i][j].append( (Dn[0][i][j][k] - Dn[1][i][j][k]) )
				# Dn[0] is D+ , Dn[1] is D-
	
	
	return EVAL, EVEC, dD


## Calculate Gruneisen parameter

def GruCalc ( Gin, q, Darray):

	#q, Darray = ReadDynMat ( nat, amass, dir)  # get dynamical matrices (eq, +, and -)
	
	V = Gin.V
	nat = Gin.nat
	amass = Gin.m
	BZ_path = Gin.BZ_path

	eval_eq, evec_eq, dD = Get_Eval_Evec_dDdV ( Darray, BZ_path)  # get equilibrium eigenvalues
											   # and eigenvectors as well as the
												   # dD matrix
	evec_eq = np.asarray(evec_eq)
			
	
	gru = []
	gru.append([]) # for the q point column
	
	
	for i in xrange( len(dD) ):  ## should be equal to the number of q points
		
		gru[0].append(BZ_path[i])
	
		
		# SORTING of eigenvalues: must correspond to eigenvectors whose inner product
		# with that of previous q point is 1
		#  e.g. < eig1(q=0) | eig1(q=1) >   = 1
		#       < eig1(q=0) | eig2(q=1) >   = 0
		
		index = []
		sort = []
		if i > 0:
	
			for x in xrange( len(evec_eq[i]) ):

				temp = [] 
				proj = []
	
				for y in xrange( len(evec_eq[i-1]) ):
						
					# Project, i.e. take the inner product of the two vectors
					p = np.vdot( evec_eq[i][:,x].transpose() , evec_eq[i-1][:,y] )
					proj.append( abs(p) )
				
				for y in xrange( len(proj) ):
								
					if proj[y] == max(proj):
						index.append([proj[y],x,y])

					
			#print index, i			
		
			'''
			# really NOT confident this sorting part works entirely
		 	for b in range(len(index)):
		 		t = [b,b]
		 		
		 		for a in range(len(index)):
		 			pr = 0.0
		 			if index[a][2] == b:
		 				if index[a][0] > pr:
		 					
		 					pr = index[a][0]
		 					t = [a,b]
					
		 		
		 		sort.append(t)		
		 	'''	

		#print sort, i
		 				
				
		 	
		########
		
		
		if i == 0:  # the first q point
		
			for j in xrange(  len(dD[i])  ):  ## 3N

				gru.append([])

				evec_0 = np.asarray( evec_eq[i] )  # 3N
				bra = evec_0[:,j]
				ket = evec_0[:,j].transpose()
				
				d_eval = np.vdot( bra, (np.dot(dD[i] , ket) ) ).real
				
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

## Calculate Gruneisen parameter

def GruCalc ( Gin, q, Darray):

	#q, Darray = ReadDynMat ( nat, amass, dir)  # get dynamical matrices (eq, +, and -)
	
	V = Gin.V
	nat = Gin.nat
	amass = Gin.m
	BZ_path = Gin.BZ_path
	
	
	
	eval_eq, evec_eq, dD = Get_Eval_Evec_dDdV ( Darray, BZ_path)  # get equilibrium eigenvalues
												   # and eigenvectors as well as the
												   # dD matrix
	gru = []
	gru.append([]) # for the q point column
	
	
	for i in xrange( len(dD) ):  ## should be equal to the number of q points
		
		
		
		
		
		#gru[0].append(i+1) # append q point number (not the actual q point)
		gru[0].append(BZ_path[i])
		
		
		
		
		
		
		
		
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
	
'''			
