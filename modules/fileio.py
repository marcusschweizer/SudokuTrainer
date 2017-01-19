import os
from .Sudoku import *
import numpy as np


class fileio(object):
	"""[summary]
	
	[description]
	""" 

		

	def to_file(sudoku, filename):

		fout = open(filename, "w")

		fout.write(str(sudoku))
		fout.write("\n")
		fout.close()

		#np.savetxt(filename, sudoku.board, fmt='%d')


	def from_file(filename):
		if not os.path.exists(filename):
			raise IOError("File not found")
			return
		fin = open(filename)

		sudoku_strings = []
		cur_string = ""
		i = 0
		line_num = 0

		for line in fin:
			cur_string += line
			line_num += 1
			if line_num%9 == 0:
				sudoku_strings.append(cur_string)
				cur_string = ""
				i += 1

		fin.close()


		sudokus = []
		for sudoku_string in sudoku_strings:
			sudokus.append(Sudoku(str_board=sudoku_string))


		#sud.board = np.loadtxt(filename, dtype=int)

		return sudokus