# Class for full sudoku
import sys
from termcolor import colored, cprint
from single_field import Field

class Sudoku():
    def __init__(self):
        self.field = [[Field() for i in range(9)] for j in range(9)]

    def get_candidates(self):
        for i in range(9):
            for j in range(9):
                if self.field[i][j].num is None:
                    for cand in range(1,10):
                        if self.try_row(cand, i) or self.try_col(cand, j) or self.try_box(cand, i, j):
                            self.field[i][j].delPos(cand)

    ''' HELPER FUNCTIONS '''
    def try_row(self, cand, row):
        check = False
        for j in range(9):
            if cand == self.field[row][j].num: check = True
        return check

    def try_col(self, cand, col):
        check = False
        for i in range(9):
            if cand == self.field[i][col].num: check = True
        return check

    def try_box(self, cand, row, col):
        check = False
        for id in self.get_box_ids(row, col):
            i,j = id
            if cand == self.field[i][j].num: check = True
        return check

    def get_box_ids(self, row, col):
        base_row = row - row%3
        base_col = col - col%3
        ids = list()
        for i in range(base_row, base_row+3):
            for j in range(base_col, base_col+3):
                ids.append((i,j))
        return ids

    ''' PRINT FUNCTIONS '''
    def __str__(self):
        str = "#####################"
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
