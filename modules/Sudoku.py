
import random



class Sudoku(object):


	def __init__(self):
		self.board = [[None]*9 for i in range(9)]
		

	def __str__(self):		
		newrow = "+" + ("-"*11 + "+")*3 + "\n"
		ret_str = newrow
		for row in range(9):
			ret_str += "| "
			for col in range(9):
				ret_str += (str(self.board[row][col]) if self.board[row][col] is not None else " ")
				ret_str += ((" | " if (col+1)%3 == 0 else " | ") if col<8 else "")
			ret_str += " |" + (("\n" + newrow) if (row+1)%3 == 0 else "\n")
		return ret_str


	def generate_random(self):
		for row in range(9):
			for col in range(9):
				number = random.randrange(0,9)
				self.board[row][col] = number if number>0 else None
