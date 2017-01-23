
from modules.Sudoku import *
from modules.fileio import *
import os
from sys import platform
import time




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

	data_file = "data/example.txt"

	#fileio.to_file(sud1, data_file)


	suds = fileio.from_file(data_file)
	suds = [sud for sud in suds if not sud.is_empty()]

	sudoku = suds[0]

	print(sudoku.print_board())

	still_changing = False
	success = False
	while (still_changing):
		still_changing = False
	
		success = sudoku.alg_OnlyOptionByBlock()
		if success:
			time.sleep(0.5)
			clear()
			print("Running Sudoku Trainer:")
			print(sudoku.print_board())
			still_changing = True

			

if __name__ == '__main__':
	main()