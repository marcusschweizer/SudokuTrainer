from .Sudoku import *


class SudokuGenerator(object):
    """Generates correct sudoku boards
    """

    @staticmethod
    def generate_random(sudoku):
        """Generates a random board, may not be solvable

        Arguments:
                sudoku {Sudoku} -- Sudoku to have board generated
        """
        for row in range(9):
            for col in range(9):
                sudoku[row, col] = random.randrange(0, 9)
