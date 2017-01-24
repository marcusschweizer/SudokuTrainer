
from modules.Sudoku import *
from modules.SudokuSolver import *
from modules.fileio import *
from modules.helper import *


import time




def main():
	



	
	clear_terminal()

	print("Running Sudoku Trainer:")

	data_file = "data/example.txt"

	#fileio.to_file(sud1, data_file)


	suds = fileio.from_file(data_file)
	suds = [sud for sud in suds if not sud.is_empty()]

	sudoku = suds[0]

	print(sudoku.print_board())

	
	SudokuSolver.solve(sudoku, print_to_terminal=True)
	
"""
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
			still_changing = True"""

			

if __name__ == '__main__':
	main()