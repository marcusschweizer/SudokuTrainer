
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

	sudoku = suds[1]

	print(sudoku.print_board())

	SudokuSolver.solve(sudoku, print_to_terminal=True, print_wait_time=0)


if __name__ == '__main__':
	main()