
from .Sudoku import *




class SudokuSolver(object):

    @staticmethod
    def solve(sudoku, print_to_terminal=False, print_wait_time=0):
        still_changing = True
        while (still_changing):
            still_changing = SudokuSolver.alg_OnlyOptionByBlock(sudoku)
            if print_to_terminal:
                time.sleep(print_wait_time)
                clear_terminal()
                print(sudoku.print_board())



    def alg_OnlyOptionByBlock(sudoku):
        success = False
        for num in range(1,10):
            if SudokuSolver.alg_OnlyOptionByBlock_PerNum(sudoku, num):
                success = True
        return success

    def alg_OnlyOptionByBlock_PerNum(sudoku, num):
        success = False
        for row in range(3):
            for col in range(3):
                if SudokuSolver.alg_OnlyOptionByBlock_PerBlockNum(sudoku, row, col, num):
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

        print("Helloworld")

        for num in range(1,10):
            num_true = 0
            num_false = 0
            current_col = 0
            col = -1
            if not sudoku.row_contains(row, num):
                for cell in sudoku[row, :]:
                    if cell == 0:
                        if not sudoku.col_contains(current_col, num):
                            num_true += 1
                            col = current_col
                        else:
                            num_false += 1
                    current_col += 1
            print(row, num_true, num_false, col, num)
            if num_true == 1:
                print("found!")