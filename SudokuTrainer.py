
from modules.Sudoku import *
from modules.fileio import *
import os
from sys import platform





def main():
	
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

	print("Running Sudoku Trainer:")
	sud1 = Sudoku()
	sud1.generate_random()
	Sudoku.print(sud1)
	print(sud1)
	#print(sud1.board2)
	#
	data_file = "data/example.txt"

	fileio.to_file(sud1, data_file)
	sud2 = fileio.from_file(data_file)

	print(sud2)


if __name__ == '__main__':
	main()