__version__ 	= "1.1.1"
__author__ 		= ['Sergio Copeto']
__credits__ 	= ["Sergio Copeto"]
__license__ 	= "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>"
__maintainer__ 	= ['Sergio Copeto']
__email__ 		= ['sergio.copeto']
__status__ 		= "Development"

from confapp import conf

conf += 'pybpod_alyx_module.settings'

from pybpod_alyx_module.module import Alyx as BpodModule