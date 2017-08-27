from __future__ import absolute_import
from __future__ import unicode_literals

from utils.exceptions import IllegalMoveException

# Considering game more than 3X3
# Than we will have to implement other algorithm
BOARD_SIZE = 3
EMPTY_CELL = '   '
X_CELL = ' X '
O_CELL = ' O '
WIN_COMBINATIONS = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))


class Board(object):

    def __init__(self, x_player, o_player):
        self.x = BOARD_SIZE
        self.y = BOARD_SIZE
        self.x_player = x_player
        self.o_player = o_player
        self.board = [EMPTY_CELL] * (self.x * self.y)
        self.turn = self.x_player

    def move(self, row, column, user):
        if self.turn != user:
            raise IllegalMoveException('It is not your turn.')

        index = (BOARD_SIZE * row) + column
        if row >= self.x or column >= self.y or index < 0:
            raise IllegalMoveException('Invalid coordinates.')
        if self.board[index] != EMPTY_CELL:
            raise IllegalMoveException('This cell is already taken.')
        if user == self.x_player:
            self.board[index] = X_CELL
            self.turn = self.o_player
        elif user == self.o_player:
            self.board[index] = O_CELL
            self.turn = self.x_player

    def is_complete(self):
        count = 0
        for comb in WIN_COMBINATIONS:
            if self.board[comb[0]] == self.board[comb[1]] == self.board[comb[2]] == X_CELL:
                self.turn = ''
                return True, self.x_player

            if self.board[comb[0]] == self.board[comb[1]] == self.board[comb[2]] == O_CELL:
                self.turn = ''
                return True, self.o_player
        for a in range(9):
            if self.board[a] == X_CELL or self.board[a] == O_CELL:
                count += 1
            if count == 9:
                self.turn = ''
                return True, ''
        return False, ''

    def to_string(self):
        result = ''
        for row in range(0, self.x):
            result += '|'
            for column in range(0, self.y):
                index = (BOARD_SIZE * row) + column
                result += self.board[index] + '|'
            result += '\n|--+--+--|\n'
        if not self.turn:
            result += 'The game is over.'
        else:
            result += '<@' + self.turn + '> \'s turn is next'
        return result
