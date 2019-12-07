# Main
import readchar
import sys
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
    print(sudoku)

def solve_sudoku(sudoku, limit=81):
    iterations = 0
    solved = True
    while not sudoku.is_solved():
        sudoku.naked_single()
        sudoku.hidden_single()
        sudoku.naked_pair()
        iterations += 1
        if iterations > limit:
            print("Could't be solved after more than 30 iterations")
            solved = False
            break
    return solved

if __name__== "__main__":
    sudoku = Sudoku("example_puzzles/s04a.txt")
    print(sudoku)
    #user_fill_sudoku(sudoku)
    sudoku.get_candidates()
    sudoku.print_possible()


    solved = solve_sudoku(sudoku, limit=30)
    print(sudoku)

    if solved: print("Check if correct: ", sudoku.is_correct())
