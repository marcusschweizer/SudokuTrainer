
from modules.Sudoku import *
from modules.SudokuSolver import *
from modules.SudokuGenerator import *
from modules.fileio import *
from modules.helper import *


import time




def main():
	
	clear_terminal()


	data_file = "data/example.txt"

	#fileio.to_file(sud1, data_file)
	suds = fileio.from_file(data_file)
	suds = [sud for sud in suds if not sud.is_empty()]

	sudoku = suds[4]

	print(sudoku.print_board())

	SudokuSolver.solve(sudoku, print_to_terminal=True, print_wait_time=.20)
	
	"""	
	for sud in suds:
		clear_terminal()
		print(sud.print_board())
		time.sleep(1)
		SudokuSolver.solve(sud, True, 0.1)
		time.sleep(1)
	#"""
	"""
	for sud in suds:
		print(sud.print_board())
	#"""
	"""
	sud3 = Sudoku()

	SudokuGenerator.generate_random(sud3)
	
	print(sud3.print_board())

	SudokuSolver.solve(sud3, True, 0.2)
	#"""

if __name__ == '__main__':
	main()