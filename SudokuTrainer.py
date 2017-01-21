
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
	
	still_changing = True
	while (still_changing):
		still_changing = False
		for num in range(9):
			for row in range(3):
				for col in range(3):
					success = sudoku.alg_OnlyOptionByBlock(row, col, num+1)

					if success:
						time.sleep(0.25)
						clear()
						print("Running Sudoku Trainer:")
						print(sudoku.print_board())
						#print(sudoku.print_actions())
						still_changing = True

if __name__ == '__main__':
	main()