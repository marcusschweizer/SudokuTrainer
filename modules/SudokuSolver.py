
from .Sudoku import *


class SudokuSolver(object):
    """Set of algorithms to solve Sudokus
    """

    @staticmethod
    def solve(sudoku, print_to_console=False, print_wait_time=0):
        """Runs all algorithms to solve a Sudoku

        Using a mix of all algorithms in this class to solve a sudoku
        Can output progress to a the console with pauses to make it human readable
        At the moment it runs each algorithm until it doesn't produce any more results before moving
        to the next algorithm, when no algorithm returns any result it is finished, either solved or
        unsolvable with these algorithms.

        Arguments:
            sudoku {Sudoku} -- sudoku to solve

        Keyword Arguments:
            print_to_console {bool} -- print out progress to console (default: {False})
            print_wait_time {number} -- pause output to make human readable (default: {0})
        """

        if sudoku.is_solved():
            print("Already solved!")
            return

        start_time = time.time()
        total_wait_time = 0
        start_progress = sudoku.progress()
        still_changing = True
        while (still_changing):
            change_by_block = SudokuSolver.alg_OnlyOptionByBlock(sudoku)

            if not change_by_block:
                change_by_row = SudokuSolver.alg_OnlyOptionByCol(sudoku)

            if not (change_by_block or change_by_row):
                change_by_col = SudokuSolver.alg_OnlyOptionByRow(sudoku)

            still_changing = change_by_block or change_by_row or change_by_col

            if print_to_console:
                time.sleep(print_wait_time)
                total_wait_time += print_wait_time
                clear_terminal()
                print(sudoku.print_board())
                print(sudoku.counts)
                if not sudoku.is_solved():
                    print("Solving : %.1f%%" % (sudoku.progress() * 100))

        if sudoku.is_solved():
            print("Solved! %.1f%% to %.1f%% solved in %.3f seconds!" % (
                start_progress * 100, sudoku.progress() * 100, time.time() - start_time - total_wait_time))
        else:
            print("Sorry, wasn't able to solve it completely, went from %.1f%% and %.1f%% solved" % (
                start_progress * 100, sudoku.progress() * 100))
            print(sudoku.board_possibles)

    def alg_OnlyOptionByBlock(sudoku):
        """Wrapper for Only Option by Block algorithm, look for all nums in all blocks

        Runs the Only Option by Block algorithm for every number and block

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algoirthm on

        Returns:
            bool -- true if changes were found
        """
        success = False
        for num in range(1, 10):
            if SudokuSolver.alg_OnlyOptionByBlock_PerNum(sudoku, num):
                success = True
        return success

    def alg_OnlyOptionByBlock_PerNum(sudoku, num):
        """Wrapper for Only Option by Block algorithm, looks for specific num in all blocks

        Runs the Only Option by Block algorithm for every block using the num as input

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algoirthm on
            num {int} -- (0..8) number to look for in blocks

        Returns:
            bool -- true if changes were found
        """
        success = False
        for block_row in range(3):
            for block_col in range(3):
                if SudokuSolver.alg_OnlyOptionByBlock_PerBlockNum(sudoku, block_row, block_col, num):
                    success = True
        return success

    def alg_OnlyOptionByBlock_PerBlockNum(sudoku, block_row, block_col, num):
        """Only Option by Block algorithm

        Looks through every cell in a block to see if there is one unique position that that specifc number could be in.
        Checks each cell to see if it is empty and whether that number is already in that column or row. If there is only
        one cell in that block that that number could be, that cell is set to that number and true is returned.

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on
            block_row {int} -- (0..2) block row to look through
            block_col {int} -- (0..2) block column to look through
            num {int} -- (0..8) number to look for

        Returns:
            bool -- true if one change occured
        """
        if sudoku.block_contains(block_row, block_col, num):
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), block already contains number" % (
                block_row, block_col, num))
            return False

        rows = range((block_row) * 3, (block_row) * 3 + 3)
        cols = range((block_col) * 3, (block_col) * 3 + 3)

        block = np.zeros([3, 3], dtype=bool)

        num_false = 0
        num_true = 0
        [x, y] = [-1, -1]
        for row in rows:
            for col in cols:
                if not sudoku.cell_is_empty(row, col) or sudoku.row_contains(row, num) or sudoku.col_contains(col, num):
                    block[row % 3, col % 3] = False
                    num_false += 1
                else:
                    block[row % 3, col % 3] = True
                    [x, y] = [row, col]
                    num_true += 1

        if num_true == 1:
            sudoku[x, y] = num
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), adding number to [%d, %d]" % (
                block_row, block_col, num, x + 1, y + 1))
            sudoku.actions.append(
                "Success! Adding %d to location row %d, col %d" % (num, x, y))
            return True
        elif num_true > 1:
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), too many options (%d)" % (
                block_row, block_col, num, num_true))
            return False
        else:
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), something went wrong :(" % (
                block_row, block_col, num))
            return False

    def alg_OnlyOptionByRow(sudoku):
        """Wrapper for Only Option by Row algorithm, runs algorithm for each row and number

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on

        Returns:
            bool -- true if change occured
        """
        success = False
        for row in range(9):
            if SudokuSolver.alg_OnlyOptionByRow_PerRow(sudoku, row):
                success = True
        return success

    def alg_OnlyOptionByRow_PerRow(sudoku, row):
        """Wrapper for Only Option by Row algorithm, runs algorithm for each num in specified row

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on
            row {int} -- (0..8) row to run algorithm on

        Returns:
            bool -- true if change occured
        """
        success = False
        for num in range(1, 10):
            if SudokuSolver.alg_OnlyOptionByRow_PerRowNum(sudoku, row, num):
                success = True
        return success

    def alg_OnlyOptionByRow_PerRowNum(sudoku, row, num):
        """Only Option by Row algorithm

        Looks through every cell in a row looking to see if there is a unique position for a specific num.
        First checks if num is in row then for each cell in the row: check if the cell is empty and
        if the num doesn't exist in the column or block then a possible solution is found. If there is only
        one unique location then a solution is found, num is placed in that cell and true is returned.

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on
            row {int} -- (0..8) Row to look through
            num {int} -- (1..9) Number to look for

        Returns:
            bool -- true if a change has occured
        """
        num_true = 0
        num_false = 0
        current_col = 0
        col = -1
        if not sudoku.row_contains(row, num):
            for cell in sudoku[row, :]:
                if cell == 0:
                    if not sudoku.col_contains(current_col, num) and not sudoku.block_contains_ByRowCol(row, current_col, num):
                        num_true += 1
                        col = current_col
                    else:
                        num_false += 1
                current_col += 1

        if num_true == 1:
            sudoku[row, col] = num
            sudoku.log.append("alg_OnlyOptionByRow_PerRowNum(sudoku, %d, %d), adding %d to [%d, %d]" % (
                row, num, num, row + 1, col + 1))
            sudoku.actions.append(
                "Success! Adding %d to location row %d, col %d" % (num, row, col))
            return True
        elif num_true > 1:
            sudoku.log.append(
                "alg_OnlyOptionByRow_PerRowNum(sudoku, %d, %d), too many options (%d)" % (row, num, num_true))
            return False
        else:
            sudoku.log.append(
                "alg_OnlyOptionByRow_PerRowNum(sudoku, %d, %d), something went wrong" % (row, num))
            return False

    def alg_OnlyOptionByCol(sudoku):
        """Wrapper for Only Option by Column algorithm, runs algorithm for each column and number

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on

        Returns:
            bool -- true if change occured
        """
        success = False
        for col in range(9):
            if SudokuSolver.alg_OnlyOptionByCol_PerCol(sudoku, col):
                success = True
        return success

    def alg_OnlyOptionByCol_PerCol(sudoku, col):
        """Wrapper for Only Option by Column algorithm, runs algorithm for each num in specified column

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on
            col {int} -- (0..8) column to run algorithm on

        Returns:
            bool -- true if change occured
        """
        success = False
        for num in range(1, 10):
            if SudokuSolver.alg_OnlyOptionByCol_PerColNum(sudoku, col, num):
                success = True
        return success

    def alg_OnlyOptionByCol_PerColNum(sudoku, col, num):
        """Only Option by Column algorithm

        Looks through every cell in a column looking to see if there is a unique position for a specific num.
        First checks if num is in column then for each cell in the column: check if the cell is empty and
        if the num doesn't exist in the row or block then a possible solution is found. If there is only
        one unique location then a solution is found, num is placed in that cell and true is returned.

        Arguments:
            sudoku {Sudoku} -- Sudoku to run algorithm on
            col {int} -- (0..8) Column to look through
            num {int} -- (1..9) Number to look for

        Returns:
            bool -- true if a change has occured
        """
        num_true = 0
        num_false = 0
        current_row = 0
        row = -1
        if not sudoku.col_contains(col, num):
            for cell in sudoku[:, col]:
                if cell == 0:
                    if not sudoku.row_contains(current_row, num) and not sudoku.block_contains_ByRowCol(current_row, col, num):
                        num_true += 1
                        row = current_row
                    else:
                        num_false += 1
                current_row += 1

        if num_true == 1:
            sudoku[row, col] = num
            sudoku.log.append("alg_OnlyOptionByCol_PerColNum(sudoku, %d, %d), adding %d to [%d, %d]" % (
                row, num, num, row + 1, col + 1))
            sudoku.actions.append(
                "Success! Adding %d to location row %d, col %d" % (num, row, col))
            return True
        elif num_true > 1:
            sudoku.log.append(
                "alg_OnlyOptionByCol_PerColNum(sudoku, %d, %d), too many options (%d)" % (row, num, num_true))
            return False
        else:
            sudoku.log.append(
                "alg_OnlyOptionByCol_PerColNum(sudoku, %d, %d), something went wrong" % (row, num))
            return False
