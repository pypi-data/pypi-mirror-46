from .SSObject import SSObject
from .planet_dist import planet_dist
#from .load_kernels import load_kernels
#from .relative_position import relative_position
#from .planet_geometry import planet_geometry
from .initialize_SolarSystem_db import initialize_SolarSystem_db

name = 'solarsystemMB'
__author__ = 'Matthew Burger'
__email__ = 'mburger@stsci.edu'
__version__ = '1.0.5'

# Verify database is set up correctly
try:
    initialize_SolarSystem_db()
except:
    print('database initialization failed')
