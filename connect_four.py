#! /usr/bin/env python3
from itertools import groupby, chain
import matplotlib.pyplot as plt

NONE = 0
RED = 1
YELLOW = 2


def diagonals_pos(matrix, cols, rows):
    """Get positive diagonals, going from bottom-left to top-right."""
    for di in ([(j, i - j) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if cols > i >= 0 and rows > j >= 0]


def diagonals_neg(matrix, cols, rows):
    """Get negative diagonals, going from top-left to bottom-right."""
    for di in ([(j, i - cols + j + 1) for j in range(cols)] for i in range(cols + rows - 1)):
        yield [matrix[i][j] for i, j in di if cols > i >= 0 and rows > j >= 0]


class Game:
    def __init__(self, cols=7, rows=6, required_to_win=4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = required_to_win
        self.board = [[NONE] * rows for _ in range(cols)]

    def insert(self, column, color):
        """Insert the color in the given column."""
        c = self.board[column]
        if c[0] != NONE:
            raise Exception('Column is full')

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        self.check_for_win()

    def check_for_win(self):
        """Check the current board for a winner."""
        w = self.get_winner()
        if w:
            self.print_board()
            raise Exception(w + ' won!')

    def get_winner(self):
        """Get the winner on the current board."""
        lines = (
            self.board,  # columns
            zip(*self.board),  # rows
            diagonals_pos(self.board, self.cols, self.rows),  # positive diagonals
            diagonals_neg(self.board, self.cols, self.rows)  # negative diagonals
        )

        for line in chain(*lines):
            for color, group in groupby(line):
                if color != NONE and len(list(group)) >= self.win:
                    return color

    def print_board(self):
        """Print the board."""
        red_x = []
        red_y = []
        yellow_x = []
        yellow_y = []
        for x in range(self.cols):
            for y in range(self.rows):
                if self.board[x][y] == 1:
                    red_x.append(x)
                    red_y.append(self.rows - y - 1)
                elif self.board[x][y] == 2:
                    yellow_x.append(x)
                    yellow_y.append(self.rows - y - 1)
        plt.scatter(red_x, red_y, 300, 'r')
        plt.scatter(yellow_x, yellow_y, 300, 'y')
        plt.axis([0, self.cols-1, -1, self.rows])
        plt.draw()
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
        print()


if __name__ == '__main__':
    from minimax import minimax_decision
    g = Game()
    plt.ion()
    turn = RED
    while True:
        if turn == YELLOW:
            next_move = minimax_decision(g,YELLOW)
            g.insert(next_move, turn)
        else:
            g.print_board()
            row = input('{}\'s turn: '.format('Red' if turn == RED else 'Yellow'))
            g.insert(int(row), turn)
        turn = YELLOW if turn == RED else RED
