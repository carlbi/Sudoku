# Main
import readchar
import sys
import time
from termcolor import colored, cprint
from full_sudoku import Sudoku
from single_field import Field

def user_fill_sudoku(sudoku):
    keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", " "]
    for i in range(9):
        for j in range(9):
            sudoku.field[i][j].setPlaceholder(" ")
            print(sudoku)
            input = "None"
            while not any(x in input for x in keys):
                input = readchar.readkey()
            if(input == " "):
                sudoku.field[i][j].setPlaceholder("_")
            else:
                sudoku.field[i][j].setNum(input)
                sudoku.field[i][j].fixed = True

    print(sudoku)

def solve_sudoku(sudoku, limit=81):
    iterations = 0
    solved = True
    while not sudoku.is_solved():
        sudoku.hidden_single()
        sudoku.naked_single()
        sudoku.hidden_pair()
        sudoku.naked_pair()
        sudoku.pointing_pair()
        iterations += 1
        if iterations > limit:
            print("Could't be solved after more than {} iterations".format(limit))
            #sudoku.print_possible()
            solved = False
            break
    return solved

def brute_force_sudoku(sudoku, limit=1000):
    solved = True
    sudoku.brute_force()
    return solved

def load_and_solve(name, brute_force=False):
    sudoku = Sudoku("example_puzzles/{}.txt".format(name))
    print(sudoku)
    if brute_force:
        t = time.time()
        solved = brute_force_sudoku(sudoku)
        time_to_solve = time.time() - t
    else:
        sudoku.get_candidates()
        t = time.time()
        solved = solve_sudoku(sudoku, limit=30)
        time_to_solve = time.time() - t
    print(sudoku)
    if solved:
        print("Check if correct: ", sudoku.is_correct())
        print("Solved in {} ms".format(round(time_to_solve*1000)))

def enter_and_solve(brute_force=False):
    sudoku = Sudoku()
    user_fill_sudoku(sudoku)
    print(sudoku)
    if brute_force:
        t = time.time()
        solved = brute_force_sudoku(sudoku)
        time_to_solve = time.time() - t
    else:
        sudoku.get_candidates()
        t = time.time()
        solved = solve_sudoku(sudoku, limit=30)
        time_to_solve = time.time() - t
    time_to_solve = time.time() - t
    print(sudoku)
    if solved:
        print("Check if correct: ", sudoku.is_correct())
        print("Solved in {} ms".format(round(time_to_solve*1000)))

if __name__== "__main__":
    load_and_solve("s15a", brute_force=True)
    #enter_and_solve(brute_force=True)
