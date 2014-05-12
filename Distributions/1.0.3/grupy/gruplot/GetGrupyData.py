import os


def GetGrupyData( type, calc ):

	prefix = ""
	labels = []
	data = []

	if type == 'bands':

		cwd = os.getcwd()
		
		for file in os.listdir( "%s/"%(cwd) ):
			
			if file.endswith(".grupy.bands.out"):	
				
				name = "%s/%s"%(cwd ,file)
				
				f = open(name, 'r')
				
				
				appended = False
				L_start=0
				D_start=0
				for i, line in enumerate(f):
					if i==0:
						s = line.split()
						prefix = "%s\t%s"%(s[0], calc)
						
				
					if 	"LABELS" in line and "/END LABELS" not in line:
						L_start = i
						
						
					if i > L_start and L_start != 0:
						if len( line.split() ) > 0: #i.e. there is something in the line
							s = line.split()
							if "/END LABELS" not in line:
								labels.append( [ s[0], s[1] ])
						if "/END LABELS" in line:
							L_start = 0
					
					if "%s DATA"%(calc) in line and "/END DATA" not in line:
						D_start = i
						
					if i > D_start and D_start != 0:
						if len( line.split() ) > 0:	
							s = line.split()
							
							if appended == False:
								for x in range(len(s)):
									data.append([])
								appended = True	
									
							if appended == True:
													
								if "/END DATA" not in line:
									for x in range(len(s)):
										data[x].append( s[x] )
					
						if "/END DATA" in line:
							D_start = 0
					
	if type == 'gru':

		cwd = os.getcwd()
		
		for file in os.listdir( "%s/"%(cwd) ):
			
			if file.endswith(".grupy.out"):	
				
				name = "%s/%s"%(cwd ,file)
				
				f = open(name, 'r')
				
				appended = False
				L_start=0
				D_start=0
				for i, line in enumerate(f):
					if i==0:
						s = line.split()
						prefix = s[0]
						
				
					if 	"LABELS" in line and "/END LABELS" not in line:
						L_start = i
						
						
					if i > L_start and L_start != 0:
						if len( line.split() ) > 0: #i.e. there is something in the line
							s = line.split()
							if "/END LABELS" not in line:
								labels.append( [ s[0], s[1] ])
						if "/END LABELS" in line:
							L_start = 0
					
					if "DATA" in line and "/END DATA" not in line:
						D_start = i
						
					if i > D_start and D_start != 0:
						if len( line.split() ) > 0:	
							s = line.split()
							
							if appended == False:
								for x in range(len(s)):
									data.append([])
								appended = True	
									
							if appended == True:
													
								if "/END DATA" not in line:
									for x in range(len(s)):
										data[x].append( s[x] )
					
						if "/END DATA" in line:
							D_start = 0		
			
	return prefix, labels, data								
							