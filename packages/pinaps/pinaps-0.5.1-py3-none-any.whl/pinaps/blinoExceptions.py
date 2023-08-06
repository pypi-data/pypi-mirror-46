class BlinoError(Exception):
	"""Base class for exceptions"""
	pass

class HardwareError(BlinoError):
	"""Error in """

class IOError(BlinoError):
	"""Error in input and output"""

class ParserError(BlinoError):
	"""Error in parsing of EEG Sensor packets"""

class ConfigError(BlinoError):
	"""Error in configuration of pinaps in current use"""
