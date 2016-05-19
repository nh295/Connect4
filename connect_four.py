#! /usr/bin/env python3
from itertools import groupby, chain
import matplotlib.pyplot as plt
import time

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
    plt.ion()

    def __init__(self, cols=7, rows=6, required_to_win=4):
        """Create a new game."""
        self.cols = cols
        self.rows = rows
        self.win = required_to_win
        self.board = [[NONE] * rows for _ in range(cols)]
        self.red_x = []
        self.red_y = []
        self.yellow_x = []
        self.yellow_y = []
        self.ax = None

    def insert(self, column, color):
        """Insert the color in the given column."""
        if column < 0 or column > self.cols - 1:
            raise ValueError('Invalid column')
        c = self.board[column]
        if c[0] != NONE:
            raise ValueError('Column is full')

        i = -1
        while c[i] != NONE:
            i -= 1
        c[i] = color

        self.check_for_win()

    def check_for_win(self):
        """Check the current board for a winner."""
        w = self.get_winner()
        if w:
            # self.print_board()
            return w

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
        if self.ax is None:
            fig, self.ax = plt.subplots()
        for x in range(self.cols):
            for y in range(self.rows):
                if self.board[x][y] == 1:
                    self.red_x.append(x)
                    self.red_y.append(self.rows - y - 1)
                elif self.board[x][y] == 2:
                    self.yellow_x.append(x)
                    self.yellow_y.append(self.rows - y - 1)
        plt.scatter(self.red_x, self.red_y, 800, 'r')
        plt.scatter(self.yellow_x, self.yellow_y, 800, 'y')
        self.ax.set_xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], minor=True)
        self.ax.set_yticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], minor=True)
        self.ax.set_yticklabels(['A','A','B','C','D','E','F'])
        self.ax.xaxis.grid(True, which='minor', linestyle='-')
        self.ax.yaxis.grid(True, which='minor', linestyle='-')
        plt.axis([-0.5, self.cols - 0.5, -0.5, self.rows - 0.5])
        plt.draw()
        print('  '.join(map(str, range(self.cols))))
        for y in range(self.rows):
            print('  '.join(str(self.board[x][y]) for x in range(self.cols)))
        print()
