
import random
import numpy as np
import string
import time
from .helper import *


class Sudoku(object):
    """Sudoku object

    Initialise and manipulate a sudoku board with checks and balances to fast and easy solving

    Usage:
    sudoku = Sudoku()
    sudoku[0,2] = 7
    etc...
    """

    def __init__(self, str_board="", name="Sudoku"):
        """Initialise sudoku object
        
        creates a blank board full of possiblities, you can initialise from a string containing numbers specifically formated
        
        Keyword Arguments:
            str_board {str} -- string representation of board to create with (default: {""})
            name {str} -- name this sudoku if you want (default: {"Sudoku"})
        """
        self.name = name
        self.actions = []
        self.log = []
        self.counts = { 0: 81 }
        self.board = np.zeros([9,9], dtype=int)
        self.board_possibles = [[list(range(1,10)) for row in range(9) ] for col in range(9)]
        if str_board != "":
            self.from_string(str_board)


    def from_string(self, str_board):
        """Converts a specifically formated string to a sudoku name and board
        
        Arguments:
            str_board {string} -- board string to convert to a sudoku board object
        """

        str_board = replace_all(str_board, ' )', '')
       
        if '(' in str_board:
            [ self.name, str_board ] = str_board.split('(')
        else:
            self.name = ""

        self.board = np.zeros([9,9], dtype=int)
        row = 0
        for line in str_board.split(',\n'):
            line = replace_all(line, '[]\n', '')
            col = 0
            for n in line.split(','):
                self[row, col] = int(n)
                col += 1
            row += 1
                

    def __str__(self):
        """convert board to a string that can be stored and retrieved
        
        Returns:
            string -- name and board in string format for storage and retrieval
        """
        return self.to_string()


    def __getitem__(self, rowcol_tuple):
        """retrieve a cell from the board
        
        Uses a tuple to represent row and col, call in the format sudoku[row,col]
        
        Arguments:
            rowcol_tuple {[int, int]} -- location to retrieve
        
        Returns:
            int -- number at cell location
        """
        return self.board[rowcol_tuple]


    def __setitem__(self, rowcol_tup, num):
        """set a cell on the board to a number, first checking for correctness
        
        tests to make sure:
        * number is in range
        * number is not already in the row, column or block (to keep sudoku integrety)
        
        Upon successful insert it updates the counts, the board and removes the num from 
        possibles list in the same row, column and block as insertion.
        
        Arguments:
            rowcol_tup {[int, int]} -- row, col representation of cell location
            num {int} -- number to put into location
        
        Returns:
            bool -- true if successful
        
        Raises:
            ValueError -- if something went wrong with inputs
        """
        row, col = rowcol_tup

        if num < 0 or num > 9:
            self.log.append("Number %d is too small or big" % (num))
            raise ValueError("Number is out of range, num=" + num)
            return False
        
        log_string = "[%d, %d]=%d" % (row, col, num)
        if num != 0:    
            if self.any_axis_contains(row, col, num):
                if self.row_contains(row, num):
                    self.log.append("Number exists in row" + log_string)
                    return False
                elif self.col_contains(col, num):
                    self.log.append("Number exists in column" + log_string)
                    return False
                elif self.block_contains_ByRowCol(row, col, num):
                    self.log.append("Number exists in block" + log_string)
                    return False
                else:
                    self.log.append("Something went wrong" + log_string)
                    raise ValueError("num was in any_axis_contains but not in any individual axis" + log_string)
                    return False
        
        self.log.append("Adding to board: " + log_string)

        self.counts[self.board[row, col]] -= 1
        self.counts[num] = self.counts.get(num, 0) + 1

        self.board[row, col] = num
        self.update_possibles(row, col, num)

        # TODO: check on what todo to possibles if 0 is added (ie cell is cleared)

        return True

    def __delitem__(self, rowcol_tuple):
        """Handles deletion/clearing of sudoku board cell
        
        Sets number at location to 0 (represents empty cell)
        
        Arguments:
            rowcol_tuple {[int, int]} -- row and column of cell to delete
        """
        self[rowcol_tuple] = 0


    def update_possibles(self, row, col, num):
        """Updates all possibles for adjacent associated cells when adding or removing a number from a cell
        
        Removes the num from all possible lists on the same row, column and block as the original insertion.
        If the number is 0 it will add instead of remove.
        
        Arguments:
            row {int} -- row location of number inserted
            col {int} -- column location of number inserted
            num {int} -- number that was inserted
        """

        if num > 0 and num < 10:
            for i in range(9):
                self.remove_possibles_single(row, i, num)
                self.remove_possibles_single(i, col, num)

            block_row, block_col = int(row/3)*3, int(col/3)*3
            
            for r in range(0,3):
                for c in range(0,3):
                    self.remove_possibles_single(block_row + r, block_col + c, num )
            
            self.board_possibles[row][col] = []
        elif num == 0:
            for i in range(1, 10):
                if not self.any_axis_contains(row, col, i):
                    if i not in self.board_possibles[row][col]:
                        self.board_possibles[row][col].append(i)
            self.board_possibles[row][col].sort()
            

    def remove_possibles_single(self, row, col, num):
        """Removes a a number from possibles of a single cell
        
        Arguments:
            row {int} -- row location
            col {int} -- column location
            num {int} -- number location
        """
        if num in self.board_possibles[row][col]:
            self.board_possibles[row][col].remove(num)


    def to_string(self):
        """
        Returns a string representation of the name and board to be used for saving and retrieving

        Returns:
            string -- string representation of name and board
        """
        prefix = "%s("   % self.name
        return   "%s%s)" % (prefix, np.array2string(self.board, separator=", ", prefix=prefix))


    def print_board(self):
        """Print a nicely formated sudoku board for the console
        
        TODO: look at implementing http://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python ??
    
        Returns:    
            string -- nicely formated string representation of the sudoku board
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
        """
        Returns formated string of actions performed on this sudoku

        Actions are defined as successfully adding a number to the board
        
        Returns:
            string -- formated list of actions
        """
        ret_str = "Actions:\n"
        for action in self.actions:
            ret_str += action + '\n'
        return ret_str


    def print_log(self):
        """
        Returns formated string of the log of all actions on this sudoku
        
        Returns:
            string -- formated list of the log
        """
        ret_str = "Log:\n"
        for entry in self.log:
            ret_str += entry + '\n'
        return ret_str


    def is_solved(self):
        """
        Tests sudouku to see if solved.
        
        Returns:
            bool -- true if sudoku is solved and finished
        """
        return self.counts[0] == 0
    

    def progress(self):
        """Percetange of board solved as a number between zero and one
        
        Returns:
            float -- 0-1 amount of board solved
        """
        return (1-self.counts[0]/81)


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
        """
        Tests if cell is empty.
        
        Arguments:
            row {int} -- row to test
            col {int} -- column to test
        
        Returns:
            bool -- true if cell is empty
        """
        return self[row, col] == 0


    def any_axis_contains(self, row, col, num):
        """Test if any axis adjacent to a cell contains a number
        
        Tests the cell, row, column and block adjacent to cell for a number.
        Typically to see if it is ok to add a number to a cell location.
        More efficient than using each individual method for row, col and block.
        
        Arguments:
            row {int} -- row of cell location
            col {int} -- column of cell location
            num {int} -- number to look for
        
        Returns:
            bool -- true if number is in or adjacent to cell.
        """
        
        # in row or column
        if num in self[row, 0:9] or num in self[0:9, col]:
            return True
        
        # in block
        if num in self[ ((int(row/3))*3):((int(row/3))*3+3), ((int(col/3))*3):((int(col/3))*3+3) ]:
            return True
        
        return False
            

    def row_contains(self, row, num):
        """
        Test if an entire row contains a number
        
        Arguments:
            row {int} -- row to test
            num {int} -- number to test for
        
        Returns:
            bool -- true if row contains number
        """
        return num in self[row, 0:9]


    def col_contains(self, col, num):
        """
        Test if an entire column contains a number
        
        Arguments:
            col {int} -- column to test
            num {int} -- number to test for
        
        Returns:
            bool -- true if column contains number
        """
        return num in self[0:9, col]


    
    def block_contains(self, block_row, block_col, num):
        """
        Test if a block contains a number
        
        Arguments:
            block_row {int} -- 0..2 block row
            block_col {int} -- 0..2 block column
            num {int} -- number to test for
        
        Returns:
            bool -- true if block contains number
        """
        return num in self[ ((block_row)*3):((block_row)*3+3), ((block_col)*3):((block_col)*3+3) ]


    def block_contains_ByRowCol(self, row, col, num):
        """
        Test if block contains a number, access block from standard row, column representation
        
        Arguments:
            row {int} -- row of cell in block to be tested
            col {int} -- column of cell in block to be tested
            num {int} -- number to test for
        
        Returns:
            bool -- true if block contains number
        """
        block_row, block_col = int(row/3), int(col/3)
        return self.block_contains(block_row, block_col, num)


        







