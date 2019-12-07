# Class for full sudoku
import sys
from termcolor import colored, cprint
from single_field import Field
from collections import Counter

class Sudoku():
    def __init__(self, file=None):
        self.field = [[Field() for i in range(9)] for j in range(9)]
        if file is not None:
            f = open(file, "r")
            puzzle = list()
            for line in f:
                line = line.strip('\n')
                puzzle.append(line.split(" "))
            for i in range(9):
                for j in range(9):
                    number = int(puzzle[i][j])
                    if number > 0: self.field[i][j].setNum(number)
        self.known_naked_pairs = list()

    def is_solved(self):
        solved = True
        for i in range(9):
            for j in range(9):
                if self.field[i][j].num is None: solved = False
        return solved

    def is_correct(self):
        correct = True
        for i in range(9):
            for j in range(9):
                num = self.field[i][j].num
                if self.try_row(num, i, j) or self.try_col(num, i, j) or self.try_box(num, i, j):
                    correct = False
                    print("Found error at:", i,j)
                    print("--- Row check: ", self.try_row(num, i, j))
                    print("--- Col check: ", self.try_col(num, i, j))
                    print("--- Box check: ", self.try_box(num, i, j))
        return correct



    def get_candidates(self):
        for i in range(9):
            for j in range(9):
                if self.field[i][j].num is None:
                    for cand in range(1,10):
                        if self.try_row(cand, i, j) or self.try_col(cand, i, j) or self.try_box(cand, i, j):
                            self.field[i][j].delPos(cand)

    ''' SOLVER FUNCTIONS '''
    def naked_single(self):
        for i in range(9):
            for j in range(9):
                if self.field[i][j].num is None and len(self.field[i][j].pos) == 1:
                    solution = self.field[i][j].pos[0]
                    self.new_solve(solution, i, j, "naked single"); continue


    def hidden_single(self):
        for i in range(9):
            for j in range(9):
                if self.field[i][j].num is None:
                    for cand in self.field[i][j].pos:
                        if not self.try_row(cand, i, j, pos=True):
                            self.new_solve(cand, i, j, "hidden single"); continue
                        if not self.try_col(cand, i, j, pos=True):
                            self.field[i][j].setNum(cand)
                            self.new_solve(cand, i, j, "hidden single"); continue
                        if not self.try_box(cand, i, j, pos=True):
                            self.new_solve(cand, i, j, "hidden single"); continue

    def naked_pair(self):
        # Row
        for i in range(9):
            cands = self.get_row_candidates(i)
            doubles = [x for x in cands if len(x) == 2]
            duplicate = self.find_duplicates(doubles)
            if duplicate is not None:
                np_id = (('R', i), duplicate)
                if np_id in self.known_naked_pairs: break
                print("Found naked pair in row {}: {}".format(i+1, duplicate))
                self.known_naked_pairs.append(np_id)
                for j in range(9):
                    if self.field[i][j].pos is not None:
                        if tuple(self.field[i][j].pos) != duplicate:
                            for x in duplicate: self.field[i][j].delPos(x)
        # Col
        for j in range(9):
            cands = self.get_col_candidates(j)
            doubles = [x for x in cands if len(x) == 2]
            duplicate = self.find_duplicates(doubles)
            if duplicate is not None:
                np_id = (('C', j), duplicate)
                if np_id in self.known_naked_pairs: break
                print("Found naked pair in col {}: {}".format(j+1, duplicate))
                self.known_naked_pairs.append(np_id)
                for i in range(9):
                    if self.field[i][j].pos is not None:
                        if tuple(self.field[i][j].pos) != duplicate:
                            for x in duplicate: self.field[i][j].delPos(x)
        # Box
        for I in range(0,9,3):
            for J in range(0,9,3):
                cands = self.get_box_candidates(I,J)
                doubles = [x for x in cands if len(x) == 2]
                duplicate = self.find_duplicates(doubles)
                if duplicate is not None:
                    np_id = ('B', duplicate)
                    if np_id in self.known_naked_pairs: break
                    self.known_naked_pairs.append(np_id)
                    print("Found naked pair in box:", duplicate)
                    for id in self.get_box_ids(I, J, included=True):
                        i,j = id
                        if self.field[i][j].pos is not None:
                            if tuple(self.field[i][j].pos) != duplicate:
                                for x in duplicate: self.field[i][j].delPos(x)

    ''' HELPER FUNCTIONS '''

    def new_solve(self, sol, row, col, type):
        # Sets number of field to solution and updates candidates
        self.field[row][col].setNum(sol)
        self.get_candidates()
        msg = "Found {} {} at field R{}C{}".format(type, sol, row+1, col+1)
        print(msg)



    def try_row(self, cand, row, col, pos=False):
        # check for occurences of candidate in row
        # pos = False check for numbers, pos = True check for possibles
        check = False
        for j in [x for x in range(9) if x != col]:
            if pos:
                if self.field[row][j].num is None and cand in self.field[row][j].pos: check = True
            else:
                if cand == self.field[row][j].num: check = True
        return check

    def try_col(self, cand, row, col, pos=False):
        # check for occurences of candidate in col
        # pos = False check for numbers, pos = True check for possibles
        check = False
        for i in [x for x in range(9) if x != row]:
            if pos:
                if self.field[i][col].num is None and cand in self.field[i][col].pos: check = True
            else:
                if cand == self.field[i][col].num: check = True
        return check

    def try_box(self, cand, row, col, pos=False):
        # check for occurences of candidate in box
        # pos = False check for numbers, pos = True check for possibles
        check = False
        for id in self.get_box_ids(row, col):
            i,j = id
            if pos:
                if self.field[i][j].num is None and cand in self.field[i][j].pos: check = True
            else:
                if cand == self.field[i][j].num: check = True
        return check

    def get_box_ids(self, row, col, included=False):
        # helper function for try_box to get indices of other fields in box
        base_row = row - row%3
        base_col = col - col%3
        ids = list()
        for i in range(base_row, base_row+3):
            for j in range(base_col, base_col+3):
                if included:
                     ids.append((i,j))
                else:
                     if not (i==row and j==col): ids.append((i,j))
        return ids

    def find_duplicates(self, cand_list):
    #Check if given list contains any duplicates
        cand_set = set()
        for elem in map(tuple, cand_list):
            if elem in cand_set: return elem
            else: cand_set.add(elem)
        return None

    def get_row_candidates(self, row):
        # returns a list of all possibles in given row
        row_candidates = list()
        for j in range(9):
            if self.field[row][j].pos is not None: row_candidates.append(self.field[row][j].pos)
        return row_candidates

    def get_col_candidates(self, col):
        # returns a list of all possibles in given col
        col_candidates = list()
        for i in range(9):
            if self.field[i][col].pos is not None: col_candidates.append(self.field[i][col].pos)
        return col_candidates

    def get_box_candidates(self, row, col):
        # returns a list of all possibles in given box
        box_candidates = list()
        for id in self.get_box_ids(row, col, included=True):
            i,j = id
            if self.field[i][j].pos is not None: box_candidates.append(self.field[i][j].pos)
        return box_candidates

    ''' PRINT FUNCTIONS '''
    def __str__(self):
        str = "\n#####################"
        for i in range(9):
            str += "\n\n" if i%3 == 0 else "\n"
            for j in range(9):
                if j%3 == 0: str += " "
                number = self.field[i][j].getNum()
                str += "{} ".format(number) if number is not None else "_ "
        return str + "\n\n"

    def print_possible(self):
        str = "#####################################################################"
        delimiter = "---------------------------------------------------------------------"
        for I in range(9):
            str += "\n\n" + delimiter + "\n" if I%3 == 0 else "\n"
            for i in range(3):
                str += "\n" if i%3 == 0 else "\n"
                for J in range(9):
                    str += " | " if J%3 == 0 else " "
                    for j in range(3):
                        possibles = self.field[I][J].pos
                        number = self.field[I][J].num
                        cand = 3*(i%3)+(j%3)+1
                        if number is None:
                            str += colored("{} ".format(cand), 'blue') if (cand in possibles) else "  "
                        else:
                            str += colored("{} ".format(number), 'red', attrs=['bold']) if (cand == 5) else "  "
        print(str + "\n\n")
