
import random
import numpy as np
import string
from .helper import *

class Sudoku(object):
	"""Sudoku object
	
	[description]
	"""
	
	def __init__(self, str_board = "", name = "Sudoku"):
		self.name = name
		if str_board == "":
			self.board = np.empty([9,9], dtype=int)
		else:
			[self.name, self.board] = Sudoku.from_string(str_board)


	def from_string(str_board):

		str_board = replace_all(str_board, ' )', '')

		[ name, str_board ] = str_board.split('(')

		board = []
		for line in str_board.split(',\n'):
			line = replace_all(line, '[]\n', '')
			board.append([ int(n) for n in line.split(',') ])
			
		return name, np.array(board)





	def __str__(self):		
		return self.to_string()

	def to_string(self):
		prefix = "%s("   % self.name
		return   "%s%s)" % (prefix, np.array2string(self.board, separator=", ", prefix=prefix))

	def print(s):
		"""Print a nice sudoku board to the console

		Displays a nice version of a the sudoku board for display in the console
		
		Arguments:
			s {Sudoku} -- 
		"""


		newrow = "+" + ("-"*11 + "+")*3 + "\n"
		ret_str = "Name: %s\n%s" % (s.name, newrow)
		for row in range(9):
			ret_str += "| "
			for col in range(9):
				ret_str += (str(s.board[row, col]) if s.board[row,col] != 0 else " ")
				ret_str += ((" | " if (col+1)%3 == 0 else " | ") if col<8 else "")
			ret_str += " |" + (("\n" + newrow) if (row+1)%3 == 0 else "\n")
		print( ret_str )

	def is_empty(self):
		"""Test for empty sudoku
		
		Returns:
			bool -- is sudoku board empty
		"""
		for row in range(9):
			for col in range(9):
				if self.board[row, col] > 0:
					return False
		return True



	def generate_random(self):
		"""[summary]
		
		[description]
		"""
		for row in range(9):
			for col in range(9):
				number = random.randrange(0,9)
				self.board[row, col] = number


	def check_row_for(self, row, num):
		
		for col in range(9):
			if self.board[row, col] == num:
				return True
		return False




	def check_col_for(col, num):
		for row in range(9):
			if self.board[row, col] == num:
				return True
		return False








