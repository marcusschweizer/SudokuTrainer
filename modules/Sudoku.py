
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
		self.actions = []
		self.log = []
		if str_board == "":
			self.board = np.zeros([9,9], dtype=int)
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

	def print_board(self):
		"""Print a nice sudoku board to the console

		Displays a nice version of a the sudoku board for display in the console
		
		Arguments:
			s {Sudoku} -- 
		"""
		newrow = "+" + ("-"*11 + "+")*3 + "\n"
		ret_str = "Name: %s\n%s" % (self.name, newrow)
		for row in range(9):
			ret_str += "| "
			for col in range(9):
				ret_str += (str(self.board[row, col]) if self.board[row,col] != 0 else " ")
				ret_str += ((" | " if (col+1)%3 == 0 else " | ") if col<8 else "")
			ret_str += " |" + (("\n" + newrow) if (row+1)%3 == 0 else "\n")
		return ret_str

	def print_actions(self):
		ret_str = "Actions:\n"
		for action in self.actions:
			ret_str += action + '\n'
		return ret_str

	def print_log(self):
		ret_str = "Log:\n"
		for entry in self.log:
			ret_str += entry + '\n'
		return ret_str

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

	def cell_is_empty(self, row, col):
		if self.board[row,col] == 0:
			return True
		return False


	def generate_random(self):
		for row in range(9):
			for col in range(9):
				number = random.randrange(0,9)
				self.board[row, col] = number


	def row_contains(self, row, num):				
		for col in range(9):
			if self.board[row, col] == num:
				return True
		return False


	def col_contains(self, col, num):
		for row in range(9):
			if self.board[row, col] == num:
				return True
		return False

	def area_contains(self, rows, cols, num):
		for row in rows:
			for col in cols:
				if self.board[row,col] == num:
					return True
		return False
	
	def block_contains(self, block_row, block_col, num):
		if num in self.board[ ((block_row)*3):((block_row)*3+3), ((block_col)*3):((block_col)*3+3) ]:
			return True
		return False

	def alg_OnlyOptionByBlock(self, block_row, block_col, num):
		
		if self.block_contains(block_row, block_col, num):
			self.log.append( "alg_OnlyOptionByBlock(%d, %d, %d), block already contains number" % (block_row, block_col, num) )
			return False
		
		rows = range((block_row)*3, (block_row)*3+3)
		cols = range((block_col)*3, (block_col)*3+3)
		
		block = np.zeros([3,3], dtype=bool)

		num_false = 0
		num_true = 0
		[x, y] = [-1, -1]
		for row in rows:
			for col in cols:
				if self.row_contains(row, num) or self.col_contains(col, num) or not self.cell_is_empty(row, col):
					block[row%3, col%3] = False
					num_false += 1
				else:
					block[row%3, col%3] = True
					[x, y] = [row, col]
					num_true += 1
		
		if num_true == 1:
			self.board[x,y] = num
			self.log.append("alg_OnlyOptionByBlock(%d, %d, %d), adding number to [%d, %d]" % (block_row, block_col, num, x+1, y+1) )
			self.actions.append("Success! Adding %d to location row %d, col %d" % (num, x, y) )
			return True
		elif num_true > 1:
			self.log.append("alg_OnlyOptionByBlock(%d, %d, %d), too many options (%d)" % (block_row, block_col, num, num_true) )
			return False
		else:
			self.log.append("alg_OnlyOptionByBlock(%d, %d, %d), something went wrong :(" % (block_row, block_col, num) )
			return False

		


		







