import os
import logging


class initialise(object):
	"""
Logger Class for info, error and debug

defaults: 

LOG_DIR = '~/log'

INFO_LOG_FILE = 'LOG_DIR + /info.log'

ERROR_LOG_FILE = 'LOG_DIR + /error.log'

DEBUG_LOG_FILE = 'LOG_DIR + /debug.log'
	
custom:

LOG_DIR = '/User/username/customfolder/log'

INFO_LOG_FILE = 'information_log.log'

ERROR_LOG_FILE = 'error_log.log'

DEBUG_LOG_FILE = 'debug_log.log'
    """	
	
	def __init__(self, LOG_DIR='', INFO_LOG_FILE='', ERROR_LOG_FILE='', DEBUG_LOG_FILE=''):
		"""
		Logger for info, error, and debug
		
		"""	
		if not LOG_DIR:
			LOG_DIR = os.path.expanduser('~/log')
		
		if not INFO_LOG_FILE:
			INFO_LOG_FILE = LOG_DIR + '/info.log'

		if not ERROR_LOG_FILE:
			ERROR_LOG_FILE = LOG_DIR + '/error.log'
			
		if not DEBUG_LOG_FILE:
			DEBUG_LOG_FILE = LOG_DIR + '/debug.log'

		self.LOG_DIR = LOG_DIR
		self.INFO_LOG_FILE = INFO_LOG_FILE
		self.ERROR_LOG_FILE = ERROR_LOG_FILE
		self.DEBUG_LOG_FILE = DEBUG_LOG_FILE
	
		if not os.path.exists(LOG_DIR):
			os.makedirs(LOG_DIR)
			os.chmod(LOG_DIR, 0o700)
			open(INFO_LOG_FILE,'a').close()
			open(ERROR_LOG_FILE,'a').close()
			open(DEBUG_LOG_FILE,'a').close()
		if not os.path.exists(ERROR_LOG_FILE):
			open(INFO_LOG_FILE,'a').close()
		elif not os.path.exists(INFO_LOG_FILE):
			open(ERROR_LOG_FILE,'a').close()
		elif not os.path.exists(DEBUG_LOG_FILE):
			open(DEBUG_LOG_FILE,'a').close()

		# set up formatting
		formatter = logging.Formatter('[%(asctime)s] %(module)s: %(message)s')
		
		# set up logging to a file for all levels WARNING and higher
		fh = logging.FileHandler(INFO_LOG_FILE)
		fh.setLevel(logging.INFO)
		fh.setFormatter(formatter)
		
		fh2 = logging.FileHandler(ERROR_LOG_FILE)
		fh2.setLevel(logging.ERROR)
		fh2.setFormatter(formatter)
		
		fh3 = logging.FileHandler(DEBUG_LOG_FILE)
		fh3.setLevel(logging.DEBUG)
		fh3.setFormatter(formatter)
		
		
		# create Logger object
		myloggerINFO = logging.getLogger('MyLogger1')
		myloggerERROR = logging.getLogger('MyLogger2')
		myloggerDEBUG = logging.getLogger('MyLogger3')
		
		# create levels
		myloggerINFO.setLevel(logging.INFO)
		myloggerINFO.addHandler(fh)
		
		myloggerERROR.setLevel(logging.ERROR)
		myloggerERROR.addHandler(fh2)
		
		myloggerDEBUG.setLevel(logging.DEBUG)
		myloggerDEBUG.addHandler(fh3)
		
		# create shortcut functions
		self.info = myloggerINFO.info
		self.error = myloggerERROR.error
		self.debug = myloggerDEBUG.debug
		