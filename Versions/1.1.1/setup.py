from distutils.core import setup, Extension
import numpy



setup(name='grupy',
	  version='1.0.3',
	  description='This is grupy',
	  author='Alex Miller',
	  author_email='asmiller1989@gmail.com',
	  url='n/a',
	  packages=['grupy', 'grupy.qe'],
	  scripts=['scripts/grupy', 'scripts/gruplot'],
	  
	  )
	  