from distutils.core import setup, Extension
import numpy



setup(name='grupy',
	  version='1.1.3',
	  description='This is grupy',
	  author='Alex Miller',
	  author_email='asmiller1989@gmail.com',
	  url='n/a',
	  packages=['grupy', 'grupy.gruplot', 'grupy.grupy_in', 
	  	'grupy.grupy_out', 'grupy.qe', 'grupy.velocity'],
	  scripts=['scripts/grupy', 'scripts/gruplot'],
	  
	  )
	  