
import os
from sys import platform


def replace_all(string, old, new=''):
	"""
	Replace each char in old with that in new.
	
	Arguments:
		string {string} -- string with chars to be replaced
		old {string} -- list of chars to look for
	
	Keyword Arguments:
		new {str} -- string to replace each char with (default: {''})
	
	Returns:
		string -- string with chars replaced
	"""
	for char in old:
		string = string.replace(char, new)
	return string


def clear_terminal():
	"""
	Clears the console regardless of platform
	"""
	if platform == "linux" or platform == "linux2":
		# linuxux
		clear = lambda: os.system('clear')
	elif platform == "darwin":
		# OS X
	    clear = lambda: os.system('clear')
	elif platform == "win32":
		# Windows...
	    clear = lambda: os.system('cls')
	
	clear()
