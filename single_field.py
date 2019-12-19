# Class for single field in sudoku

class Field():
    def __init__(self, number=None):
        self.num = number
        self.pos = list(range(1,10))
        self.placeholder = None # Used for user fill only
        self.fixed = False # Used only for brute force

    def __str__(self):
        return "num = {}, pos = {}".format(self.num, self.pos)

    ''' SETTERS '''
    def setNum(self, number):
        self.num = int(number)
        self.pos = None

    def setPlaceholder(self, placeholder):
        self.placeholder = placeholder

    ''' GETTERS '''
    def getNum(self):
        if self.num is not None:
            return self.num
        else:
            return self.placeholder

    ''' DELETE '''
    def delPos(self, possible):
        if possible in self.pos:
            self.pos.remove(possible)
