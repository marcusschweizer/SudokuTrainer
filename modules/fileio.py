import os
from .Sudoku import *
import numpy as np


class fileio(object):
	"""
	Handles file input and output for the SudokuTraininer app
	""" 

		

	def to_file(sudoku, filename):
		"""Prints a sudoku (name and board) to a file specified

		TODO: this overwrites current file, should append to end
		
		Arguments:
			sudoku {Sudoku} -- Sudoku object to be saved
			filename {string} -- File to write to
		"""

		fout = open(filename, "w")

		fout.write(sudoku.to_string())
		fout.write("\n")
		fout.close()


	def from_file(filename):
		"""Read formated sodukus from a file
		
		Arguments:
			filename {string} -- file to read from
		
		Returns:
			Sudoku[] -- List of Sudokus
		
		Raises:
			IOError -- If file doesn't exist
		"""
		if not os.path.exists(filename):
			raise IOError("File not found")
			return
		fin = open(filename)

		sudoku_strings = []
		cur_string = ""
		i = 0
		line_num = 0

		# read 9 lines at a time into a single sudoku
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

		return sudokus












