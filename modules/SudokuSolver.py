
from .Sudoku import *


class SudokuSolver(object):

    @staticmethod
    def solve(sudoku, print_to_terminal=False, print_wait_time=0):
        
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
                    # not sure if required, essentially same algorithm as by row?

            still_changing = change_by_block or change_by_row or change_by_col
        
            if print_to_terminal:
                time.sleep(print_wait_time)
                total_wait_time += print_wait_time
                clear_terminal()
                print(sudoku.print_board())
                print(sudoku.counts)
                if not sudoku.is_solved():
                    print("Solving : %.1f%%" % (sudoku.progress()*100))

        if sudoku.is_solved():
            print("Solved! %.1f%% to %.1f%% solved in %.3f seconds!" % (start_progress*100, sudoku.progress()*100, time.time() - start_time - total_wait_time) )
        else:
            print("Sorry, wasn't able to solve it completely, went from %.1f%% and %.1f%% solved" % (start_progress*100, sudoku.progress()*100))
            print(sudoku.board_possibles)

    def alg_OnlyOptionByBlock(sudoku):
        success = False
        for num in range(1,10):
            if SudokuSolver.alg_OnlyOptionByBlock_PerNum(sudoku, num):
                success = True
        return success

    def alg_OnlyOptionByBlock_PerNum(sudoku, num):
        success = False
        for block_row in range(3):
            for block_col in range(3):
                if SudokuSolver.alg_OnlyOptionByBlock_PerBlockNum(sudoku, block_row, block_col, num):
                    success = True
        return success
                    
    def alg_OnlyOptionByBlock_PerBlockNum(sudoku, block_row, block_col, num):
        
        if sudoku.block_contains(block_row, block_col, num):
            sudoku.log.append( "alg_OnlyOptionByBlock(%d, %d, %d), block already contains number" % (block_row, block_col, num) )
            return False
        
        rows = range((block_row)*3, (block_row)*3+3)
        cols = range((block_col)*3, (block_col)*3+3)
        
        block = np.zeros([3,3], dtype=bool)

        num_false = 0
        num_true = 0
        [x, y] = [-1, -1]
        for row in rows:
            for col in cols:
                if sudoku.row_contains(row, num) or sudoku.col_contains(col, num) or not sudoku.cell_is_empty(row, col):
                    block[row%3, col%3] = False
                    num_false += 1
                else:
                    block[row%3, col%3] = True
                    [x, y] = [row, col]
                    num_true += 1
        
        if num_true == 1:
            sudoku[x,y] = num
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), adding number to [%d, %d]" % (block_row, block_col, num, x+1, y+1) )
            sudoku.actions.append("Success! Adding %d to location row %d, col %d" % (num, x, y) )
            return True
        elif num_true > 1:
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), too many options (%d)" % (block_row, block_col, num, num_true) )
            return False
        else:
            sudoku.log.append("alg_OnlyOptionByBlock(%d, %d, %d), something went wrong :(" % (block_row, block_col, num) )
            return False



    def alg_OnlyOptionByRow(sudoku):
        success = False
        for row in range(9):
            if SudokuSolver.alg_OnlyOptionByRow_PerRow(sudoku, row):
                success = True
        return success

    def alg_OnlyOptionByRow_PerRow(sudoku, row):
        success = False
        for num in range(1,10):
            if SudokuSolver.alg_OnlyOptionByRow_PerRowNum(sudoku, row, num):
                success = True
        return success

    def alg_OnlyOptionByRow_PerRowNum(sudoku, row, num):

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
            sudoku.log.append("alg_OnlyOptionByRow_PerRowNum(sudoku, %d, %d), adding %d to [%d, %d]" % ( row, num, num, row + 1, col + 1) )
            sudoku.actions.append("Success! Adding %d to location row %d, col %d" % (num, row, col) )
            return True
        elif num_true > 1:
            sudoku.log.append("alg_OnlyOptionByRow_PerRowNum(sudoku, %d, %d), too many options (%d)" % (row, num, num_true) )
            return False
        else:
            sudoku.log.append("alg_OnlyOptionByRow_PerRowNum(sudoku, %d, %d), something went wrong" % (row, num) )
            return False


    def alg_OnlyOptionByCol(sudoku):
        success = False
        for col in range(9):
            if SudokuSolver.alg_OnlyOptionByCol_PerCol(sudoku, col):
                success = True
        return success

    def alg_OnlyOptionByCol_PerCol(sudoku, col):
        success = False
        for num in range(1,10):
            if SudokuSolver.alg_OnlyOptionByCol_PerColNum(sudoku, col, num):
                success = True
        return success

    def alg_OnlyOptionByCol_PerColNum(sudoku, col, num):
        
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
            sudoku.log.append("alg_OnlyOptionByCol_PerColNum(sudoku, %d, %d), adding %d to [%d, %d]" % ( row, num, num, row + 1, col + 1) )
            sudoku.actions.append("Success! Adding %d to location row %d, col %d" % (num, row, col) )
            return True
        elif num_true > 1:
            sudoku.log.append("alg_OnlyOptionByCol_PerColNum(sudoku, %d, %d), too many options (%d)" % (row, num, num_true) )
            return False
        else:
            sudoku.log.append("alg_OnlyOptionByCol_PerColNum(sudoku, %d, %d), something went wrong" % (row, num) )
            return False