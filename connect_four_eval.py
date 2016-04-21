# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 20:19:44 2016

@author: Bang
"""
from itertools import groupby, chain
from connect_four import diagonals_pos as diag_pos
from connect_four import diagonals_neg as diag_neg


NONE = 0
RED = 1
YELLOW = 2  

def evaluate(board,player,cols,rows):
    
    if player==RED:
        opponent=YELLOW
    else:
        opponent=RED

    lines = (
        board,  # columns
        zip(*board),  # rows
        diag_pos(board, cols, rows),  # positive diagonals
        diag_neg(board, cols, rows)  # negative diagonals
    )
    
    score = 0
    
    for line in chain(*lines):
        for color, group in groupby(line):
            if color == player and len(list(group)) == 2:
                score = score + 100
            elif color == player and len(list(group)) == 3:
                score = score + 300
            elif color == player and len(list(group)) >= 4:
                score = score + 10000
                
            if color == opponent and len(list(group)) == 2:
                score = score - 200
            elif color == opponent and len(list(group)) == 3:
                score = score - 500
            elif color == opponent and len(list(group)) >= 4:
                score = score - 30000
                
    return score