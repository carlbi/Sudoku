# Class for full sudoku
import sys
import math
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
        self.known_hidden_pairs = list()
        self.known_pointing_pairs = list()

    ''' STANDARD FUNCTIONS '''

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
            doubles = [x for x in cands if x is not None and len(x) == 2]
            duplicate = self.find_duplicates(doubles)
            if duplicate is not None:
                np_id = (('R', i), duplicate)
                if np_id in self.known_naked_pairs: continue
                self.known_naked_pairs.append(np_id)
                print("Found naked pair in row {}: {}".format(i+1, duplicate))
                for j in range(9):
                    if self.field[i][j].pos is not None:
                        if tuple(self.field[i][j].pos) != duplicate:
                            for x in duplicate: self.field[i][j].delPos(x)
        # Col
        for j in range(9):
            cands = self.get_col_candidates(j)
            doubles = [x for x in cands if x is not None and len(x) == 2]
            duplicate = self.find_duplicates(doubles)
            if duplicate is not None:
                np_id = (('C', j), duplicate)
                if np_id in self.known_naked_pairs: continue
                self.known_naked_pairs.append(np_id)
                print("Found naked pair in col {}: {}".format(j+1, duplicate))
                for i in range(9):
                    if self.field[i][j].pos is not None:
                        if tuple(self.field[i][j].pos) != duplicate:
                            for x in duplicate: self.field[i][j].delPos(x)
        # Box
        for I in range(0,9,3):
            for J in range(0,9,3):
                cands = self.get_box_candidates(I,J)
                doubles = [x for x in cands if x is not None and len(x) == 2]
                duplicate = self.find_duplicates(doubles)
                if duplicate is not None:
                    np_id = ('B', duplicate)
                    if np_id in self.known_naked_pairs: continue
                    self.known_naked_pairs.append(np_id)
                    print("Found naked pair in box:", duplicate)
                    for id in self.get_box_ids(I, J, included=True):
                        i,j = id
                        if self.field[i][j].pos is not None:
                            if tuple(self.field[i][j].pos) != duplicate:
                                for x in duplicate: self.field[i][j].delPos(x)
    def hidden_pair(self):
        # Row
        for i in range(9):
            cands = self.get_row_candidates(i)
            hidden_double = self.hidden_in_list(cands)
            if len(hidden_double) == 2:
                hp_id = ('B', hidden_double)
                if hp_id in self.known_hidden_pairs: continue
                self.known_hidden_pairs.append(hp_id)
                print("Found hidden pair in row {}: {}".format(i+1, hidden_double))
                for j in range(9):
                    if self.field[i][j].pos is not None:
                        if hidden_double[0] in self.field[i][j].pos and hidden_double[1] in self.field[i][j].pos:
                            self.field[i][j].pos = [hidden_double[0], hidden_double[1]]

        # Col
        for j in range(9):
            cands = self.get_col_candidates(j)
            hidden_double = self.hidden_in_list(cands)
            if len(hidden_double) == 2:
                hp_id = ('B', hidden_double)
                if hp_id in self.known_hidden_pairs: continue
                self.known_hidden_pairs.append(hp_id)
                print("Found hidden pair in col {}: {}".format(j+1, hidden_double))
                for i in range(9):
                    if self.field[i][j].pos is not None:
                        if hidden_double[0] in self.field[i][j].pos and hidden_double[1] in self.field[i][j].pos:
                            self.field[i][j].pos = [hidden_double[0], hidden_double[1]]

        # Box
        for I in range(0,9,3):
            for J in range(0,9,3):
                cands = self.get_box_candidates(I,J)
                hidden_double = self.hidden_in_list(cands)
                if len(hidden_double) == 2:
                    hp_id = ('B', hidden_double)
                    if hp_id in self.known_hidden_pairs: continue
                    self.known_hidden_pairs.append(hp_id)
                    print("Found hidden pair in box: {}".format(hidden_double))
                    for id in self.get_box_ids(I, J, included=True):
                        i,j = id
                        if self.field[i][j].pos is not None:
                            if hidden_double[0] in self.field[i][j].pos and hidden_double[1] in self.field[i][j].pos:
                                self.field[i][j].pos = [hidden_double[0], hidden_double[1]]

    def pointing_pair(self):
        # Row
        for I in range(9):
            cands = self.get_row_candidates(I)
            occurences = [None]*9
            for num in range(9):
                occurences[num] = [x for x in range(9) if cands[x] is not None and cands[x].count(num+1) != 0]
                for box in range(3):
                    if len(occurences[num]) > 1 and all(math.floor(J/3) == box for J in occurences[num]):
                        for id in self.get_box_ids(I, box*3):
                            i, j = id
                            if i != I and self.field[i][j].pos is not None :
                                pp_id = (('R', I), num+1)
                                if pp_id in self.known_pointing_pairs: continue
                                self.known_pointing_pairs.append(pp_id)
                                print("Found pointing pair in row {}: {}".format(I+1, num+1))
                                self.field[i][j].delPos(num+1)
        # Col
        for J in range(9):
            cands = self.get_col_candidates(J)
            occurences = [None]*9
            for num in range(9):
                occurences[num] = [x for x in range(9) if cands[x] is not None and cands[x].count(num+1) != 0]
                for box in range(3):
                    if len(occurences[num]) > 1 and all(math.floor(I/3) == box for I in occurences[num]):
                        for id in self.get_box_ids(box*3, J):
                            i, j = id
                            if j != J and self.field[i][j].pos is not None :
                                pp_id = (('C', J), num+1)
                                if pp_id in self.known_pointing_pairs: continue
                                self.known_pointing_pairs.append(pp_id)
                                print("Found pointing pair in col {}: {}".format(J+1, num+1))
                                self.field[i][j].delPos(num+1)

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
        # helper function to get indices of other fields in box
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

    def hidden_in_list(self, cands):
        occurences = [None]*9
        for num in range(9):
            occurences[num] = [x for x in range(9) if cands[x] is not None and cands[x].count(num+1) != 0]
            if len(occurences[num]) != 2: occurences[num] = None
        hidden_double = list()
        for num in range(9):
            if occurences[num] is not None and occurences.count(occurences[num]) > 1:
                hidden_double.append(num+1)
        return hidden_double

    def get_row_candidates(self, row):
        # returns a list of all possibles in given row
        row_candidates = list()
        for j in range(9):
            if self.field[row][j].pos is not None:
                row_candidates.append(self.field[row][j].pos)
            else:
                row_candidates.append(None)
        return row_candidates

    def get_col_candidates(self, col):
        # returns a list of all possibles in given col
        col_candidates = list()
        for i in range(9):
            if self.field[i][col].pos is not None:
                col_candidates.append(self.field[i][col].pos)
            else:
                col_candidates.append(None)
        return col_candidates

    def get_box_candidates(self, row, col):
        # returns a list of all possibles in given box
        box_candidates = list()
        for id in self.get_box_ids(row, col, included=True):
            i,j = id
            if self.field[i][j].pos is not None:
                box_candidates.append(self.field[i][j].pos)
            else:
                box_candidates.append(None)
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
