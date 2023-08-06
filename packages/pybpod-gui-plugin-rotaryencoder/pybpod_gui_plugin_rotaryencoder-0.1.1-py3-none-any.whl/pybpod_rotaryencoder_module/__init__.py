__version__ 	= "0.1.1"
__author__ 		= ['Ricardo Ribeiro']
__credits__ 	= ["Ricardo Ribeiro"]
__license__ 	= "Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>"
__maintainer__ 	= ['Ricardo Ribeiro']
__email__ 		= ['ricardojvr@gmail.com']
__status__ 		= "Development"

from confapp import conf

conf += 'pybpod_rotaryencoder_module.settings'

from pybpod_rotaryencoder_module.module import RotaryEncoder as BpodModule