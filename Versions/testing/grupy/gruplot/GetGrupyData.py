import os
import json


def GetGrupyData( type, calc ):
	if type == 'gru':
		end = '.grupy.out'
	elif type == 'bands':
		end = '.grupy.bands.out'	
	
	prefix = ""
	labels = []
	data = []
	q = []
	mode_i = []

	cwd = os.getcwd()
	
	for file in os.listdir( "%s/"%(cwd) ):	
		
		if file.endswith('%s'%end):	
				
			name = "%s/%s"%(cwd ,file)
				
			with open(name, 'r') as file:
				
				num_modes = 0
					
				for line in file:
					l = json.loads(line)
					
					if 'label_q' in l:
						labels.append(l)
						prefix = l['prefix']
						num_modes = int( l['num_modes'] )
						
					
					elif calc and 'Calculation' in l:
						if l['Calculation'].lower() == calc.lower():
							if 'Omega' in l:
								q.append( float( l['q'] ) )
								data.append( float( l['Omega'] ) )
								mode_i.append( int( l['Mode_Index'] ) )
								
								#temp = [ float(l['q']) ]
								#for i in range( len( l['Omega'] ) ):
								#	temp.append( float(l['Omega'][i]) )
								#data.append(temp)						
					
					elif not calc:
						if 'Gru' in l:
							q.append( float( l['q'] ) )
							data.append( float( l['Gru'] )  )
							mode_i.append( int( l['Mode_Index'] ) )
							#temp = [ float(l['q']) ]
							#for i in range( len( l['Gru'] ) ):
							#	temp.append( float(l['Gru'][i]) )
							#data.append(temp)	
					
					
			
	return prefix, num_modes, labels, q, data, mode_i	

