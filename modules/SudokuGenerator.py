from .Sudoku import *


class SudokuGenerator(object):

    @staticmethod
    def generate_random(self):
		for row in range(9):
			for col in range(9):
				self[row, col] = random.randrange(0,9)

