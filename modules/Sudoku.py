
import random
import numpy as np


class Sudoku(object):
	"""Sudoku object
	
	[description]
	"""


	def __init__(self):
		#self.board = [[None]*9 for i in range(9)]
		self.board = np.empty([9,9], dtype=int)
		

	def __str__(self):		
		
		return str(self.board)

	def print(s):
		"""Print a nice sudoku board to the console

		Displays a nice version of a the sudoku board for display in the console
		
		Arguments:
			s {Sudoku} -- 
		"""
		newrow = "+" + ("-"*11 + "+")*3 + "\n"
		ret_str = newrow
		for row in range(9):
			ret_str += "| "
			for col in range(9):
				ret_str += (str(s.board[row, col]) if s.board[row,col] != 0 else " ")
				ret_str += ((" | " if (col+1)%3 == 0 else " | ") if col<8 else "")
			ret_str += " |" + (("\n" + newrow) if (row+1)%3 == 0 else "\n")
		print( ret_str )


	def generate_random(self):
		"""[summary]
		
		[description]
		"""
		for row in range(9):
			for col in range(9):
				number = random.randrange(0,9)
				self.board[row, col] = number
