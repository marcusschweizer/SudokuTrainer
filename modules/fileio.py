import os
from .Sudoku import *
import numpy as np


class fileio(object):
	"""[summary]
	
	[description]
	""" 

		

	def to_file(sudoku, filename):

		fout = open(filename, "w")

		fout.write("Sudoku 1:")
		fout.close()

		np.savetxt(filename, sudoku.board, fmt='%d')


	def from_file(filename):
		if not os.path.exists(filename):
			raise IOError("File not found")
			return
		"""fin = open(filename)

		fin.close()"""
		sud = Sudoku()

		sud.board = np.loadtxt(filename, dtype=int)

		return sud