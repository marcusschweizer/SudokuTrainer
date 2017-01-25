from .Sudoku import *


class SudokuGenerator(object):

	@staticmethod
	def generate_random(sudoku):
		for row in range(9):
			for col in range(9):
				sudoku[row, col] = random.randrange(0,9)

