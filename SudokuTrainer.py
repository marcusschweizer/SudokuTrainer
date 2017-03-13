
from modules.Sudoku import *
from modules.SudokuSolver import *
from modules.SudokuGenerator import *
from modules.fileio import *
from modules.helper import *
from tests.SudokuTesting import *

import sys, re, optparse
import time


def main(options):

    clear_terminal()

    data_file = "data/example.txt"

    #fileio.to_file(sud1, data_file)
    suds = fileio.from_file(data_file)
    suds = [sud for sud in suds if not sud.is_empty()]

    #sudoku = suds[4]

    # print(sudoku.print_board())

    #SudokuSolver.solve(sudoku, print_to_console=True, print_wait_time=0)

    #"""
    for sud in suds:
        clear_terminal()
        print(sud.print_board())
        if options.debug:
            SudokuSolver.solve(sud, True, 0.05)
            time.sleep(1)
        else:
            SudokuSolver.solve(sud, True, 0)
            time.sleep(0.5)
        

def process_args():
    first_re = re.compile(r'^\d{3}$')

    parser = optparse.OptionParser()
    parser.set_defaults(test=False, debug=False)
    parser.add_option('--test', action='store_true', dest='test')
    parser.add_option('--debug', action='store_true', dest='debug')
    (options, args) = parser.parse_args()

    if len(args) == 1:
        if first_re.match(args[0]):
            print("Primary argument is : ", args[0])
        else:
            raise ValueError("First argument should be ...")
    elif len(args) > 1:
        raise ValueError("Too many command line arguments")

    if options.test:
        print('test flag set')
    
    if options.debug:
        print('debug flag set')
    
    del sys.argv[1:]

    return options


def run_tests():
    print("Running Test Suite")

    #st = SudokuTesting()
    unittest.main()



if __name__ == '__main__':

    options = process_args()

    if options.test:
        run_tests()
    else:
        main(options)


   