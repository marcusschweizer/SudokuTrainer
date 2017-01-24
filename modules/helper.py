
import os
from sys import platform


def replace_all(string, old, new=''):
	for char in old:
		string = string.replace(char, new)
	return string

def clear_terminal():
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
