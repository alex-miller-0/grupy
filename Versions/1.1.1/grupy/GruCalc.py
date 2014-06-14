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
				
				for k in xrange( len(eval) ):  # 3N 
					# TESTING: should be 3N now
					EVAL[j].append(eval[k])
					EVEC[j].append(evec[k])
				
					
			
			else: ## i.e. NON-equilibrium matrices
				Dn[i-1].append(Darray[i][j])  ## this is a full dyn matrix
				
	
	# Dn array should have 2 columns of elements (for + and - volume calculations)
	#	, with each element being a 3Nx3N matrix of eigenvalues at that q-point
	# Deq array should have three dimensions	
	
	
	for i in xrange(len(Darray[0])):  # q points
		
		dD.append([])
		
		for j in xrange( len(Darray[0][i]) ):  # 3N
			
			dD[i].append([])
			
			for k in xrange( len(Darray[0][i][j]) ):  # 3N
			
				dD[i][j].append( (Dn[0][i][j][k] - Dn[1][i][j][k]) )
				# Dn[0] is D+ , Dn[1] is D-
	
	
	return EVAL, EVEC, dD


## Calculate Gruneisen parameter

def GruCalc ( Gin, q, Darray):

	
	V = Gin.V
	nat = Gin.nat
	amass = Gin.m
	BZ_path = Gin.BZ_path

	eval_eq, evec_eq, dD = Get_Eval_Evec_dDdV ( Darray, BZ_path)  # get equilibrium eigenvalues
											   # and eigenvectors as well as the
												   # dD matrix
	dD = np.asarray(dD)
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
				rel = []
	
				for y in xrange( len(evec_eq[i-1]) ):
						
					# Project, i.e. take the inner product of the two vectors
					p = np.vdot( evec_eq[i][:,x].transpose() , evec_eq[i-1][:,y] )
					proj.append( abs(p) )
					rel.append( [x,y])
					
				for z in xrange( len(proj) ):
						
					if proj[z] == max(proj):
						index.append([proj[z],rel[z][0], rel[z][1] ])
						

		
		if i == 0:  # the first q point
		
			for j in xrange(  len(dD[i])  ):  ## 3N

				gru.append([])

				evec_0 = np.asarray( evec_eq[i] )  # 3N
				bra = evec_0[:,j]
				ket = evec_0[:,j].transpose()
				
				d_eval = abs( np.vdot( bra, (np.dot(dD[i] , ket) ) ) )
				
				
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
				
#
# We're going through the 3N items in the index
#				
				for x in xrange( len(index) ):
#
# Check to see if the second number (i.e. the ket of the sorting projection)
# in the index is the mode we want to write a value to
#

					if index[x][1] == j: 
		
						evec_q = np.asarray( evec_eq[i])
						
						
						bra = evec_q[:,x]
						ket = evec_q[:,x].transpose()
						
						d_eval = abs( np.dot( bra, (np.dot(dD[i] , ket) ) ) )
					
						
						if abs(d_eval) < 1e-8 and abs(eval_eq[i][j]) < 1e-7:
							
							g = 0.0
			
						else:
							# may want to change to eval_eq[i][x]
							g = - ( d_eval/(2*eval_eq[i][j]) )* ( V[0]/(V[1]-V[2]))
	
						gru[j+1].append( float(g) )
				
		

	return q, gru		
	
		
