
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
		self.counts = { 0: 81 }
		self.board = np.zeros([9,9], dtype=int)
		if str_board != "":
			self.from_string(str_board)


	def from_string(self, str_board):

		str_board = replace_all(str_board, ' )', '')

		[ self.name, str_board ] = str_board.split('(')

		self.board = np.zeros([9,9], dtype=int)
		row = 0
		for line in str_board.split(',\n'):
			line = replace_all(line, '[]\n', '')
			col = 0
			for n in line.split(','):
				self[row, col] = int(n)
				col += 1
			row += 1
				
		#return name, np.array(board)


	def __str__(self):		
		return self.to_string()

	def __getitem__(self, rowcol_tup):
		row, col = rowcol_tup
		return self.board[row, col]

	def __setitem__(self, rowcol_tup, num):
		row, col = rowcol_tup

		if num < 0 or num > 9:
			self.log.append("Number %d is too small or big" % (num))
			return False
		
		log_string = "[%d, %d]=%d" % (row, col, num)
		if num != 0:	
			if self.row_contains(row, num):
				self.log.append("Number exists in row" + log_string)
				return False
			elif self.col_contains(col, num):
				self.log.append("Number exists in column" + log_string)
				return False
			elif self.block_contains_ByRowCol(row, col, num):
				self.log.append("Number exists in block" + log_string)
				return False
		
		self.log.append("Adding to board: " + log_string)
		
		self.counts[self.board[row, col]] -= 1
		self.counts[num] = self.counts.get(num, 0) + 1

		self.board[row, col] = num
		return True

	def __delitem__(self, rowcol_tup):
		row, col = rowcol_tup
		self[row, col] = 0


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
				ret_str += (str(self[row, col]) if self[row,col] != 0 else " ")
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
				if self[row, col] > 0:
					return False
		return True

	def cell_is_empty(self, row, col):
		return self[row,col] == 0


	def generate_random(self):
		for row in range(9):
			for col in range(9):
				self[row, col] = random.randrange(0,9)


	def row_contains(self, row, num):				
		for col in range(9):
			if self[row, col] == num:
				return True
		return False


	def col_contains(self, col, num):
		for row in range(9):
			if self[row, col] == num:
				return True
		return False

	def area_contains(self, rows, cols, num):
		for row in rows:
			for col in cols:
				if self[row,col] == num:
					return True
		return False
	
	def block_contains(self, block_row, block_col, num):
		return num in self[ ((block_row)*3):((block_row)*3+3), ((block_col)*3):((block_col)*3+3) ]

	def block_contains_ByRowCol(self, row, col, num):
		block_row, block_col = int(row/3), int(col/3)
		return self.block_contains(block_row, block_col, num)


	def alg_OnlyOptionByBlock(self):
		success = False
		for num in range(1,10):
			if self.alg_OnlyOptionByBlock_PerNum(num):
				success = True
		return success

	def alg_OnlyOptionByBlock_PerNum(self, num):
		success = False
		for row in range(3):
			for col in range(3):
				if self.alg_OnlyOptionByBlock_PerBlockNum(row, col, num):
					success = True
		
		return success
					

	def alg_OnlyOptionByBlock_PerBlockNum(self, block_row, block_col, num):
		
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
			self[x,y] = num
			self.log.append("alg_OnlyOptionByBlock(%d, %d, %d), adding number to [%d, %d]" % (block_row, block_col, num, x+1, y+1) )
			self.actions.append("Success! Adding %d to location row %d, col %d" % (num, x, y) )
			return True
		elif num_true > 1:
			self.log.append("alg_OnlyOptionByBlock(%d, %d, %d), too many options (%d)" % (block_row, block_col, num, num_true) )
			return False
		else:
			self.log.append("alg_OnlyOptionByBlock(%d, %d, %d), something went wrong :(" % (block_row, block_col, num) )
			return False

	
	def alg_OnlyOptionByRow(self):
		success = False
		for row in range(9):
			if self.alg_OnlyOptionByRow_PerRow(row):
				success = True
		return success

	def alg_OnlyOptionByRow_PerRow(self, row):

		print("Helloworld")

		for num in range(1,10):
			num_true = 0
			num_false = 0
			current_col = 0
			col = -1
			if not self.row_contains(row, num):
				for cell in self[row, :]:
					if cell == 0:
						if not self.col_contains(current_col, num):
							num_true += 1
							col = current_col
						else:
							num_false += 1
					current_col += 1
			print(row, num_true, num_false, col, num)
			if num_true == 1:
				print("found!")


	


		







