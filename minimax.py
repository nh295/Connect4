# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 13:53:01 2016

@author: Bang
"""
from itertools import groupby, chain
from connect_four import Game
from connect_four import diagonals_pos as diag_pos
from connect_four import diagonals_neg as diag_neg
from connect_four_eval import evaluate
from copy import deepcopy

search_depth = 10

game = Game()
rows = game.rows
cols = game.cols
required_to_win = 4

NONE = 0
RED = 1
YELLOW = 2  


def insert(board, column, color):
    """Insert the color in the given column."""  
    c = board[column]
    if c[0] != NONE:
        raise Exception('Column is full')

    i = -1
    while c[i] != NONE:
        i -= 1
    c[i] = color
    return board

def check_for_full_columns(column):
    if column[0] != NONE:
        return True
    else:
        return False

def get_winner(board):
    """Get the winner on the current board."""
    lines = (
        board,  # columns
        zip(*board),  # rows
        diag_pos(board, cols, rows),  # positive diagonals
        diag_neg(board, cols, rows)  # negative diagonals
    )

    for line in chain(*lines):
        for color, group in groupby(line):
            if color != NONE and len(list(group)) >= required_to_win:
                return color


# Minimax Search

def minimax_decision(thisGame, player):

    if player==RED:
        opponent=YELLOW
    else:
        opponent=RED
    
    def minimax(node, depth, maximizingPlayer):
        if depth == 0 or get_winner(node) != NONE:
            return evaluate(node,player,cols,rows)
        
        if maximizingPlayer:
            V = -99999
            for i in range(cols):
                if check_for_full_columns(node[i]):
                    continue
                else:
                    tmp_node = deepcopy(node)
                    childNode = insert(tmp_node,i,opponent)
                    tmpV = minimax(childNode, depth-1, False)
                    if tmpV > V:                       
                        V = tmpV
            return V
        else:
            V = 99999
            for i in range(cols):
                if check_for_full_columns(node[i]):
                    continue
                else:
                    tmp_node = deepcopy(node)
                    childNode = insert(tmp_node,i,player)
                    tmpV = minimax(childNode, depth-1, True)
                    if tmpV < V:                       
                        V = tmpV
            return V
    
    current_board = thisGame.board
    V = -99999
    for i in range(cols):
        if check_for_full_columns(current_board[i]):
            continue
        else:
            board = deepcopy(current_board)
            childNode = insert(board,i,opponent)
            tmpV = minimax(childNode, search_depth-1, False)
            if tmpV > V:                       
                V = tmpV
                nextMove = i
                
    return nextMove
        


#    player = game.to_move(state)
#
#    def max_value(state):
#        if game.terminal_test(state):
#            return game.utility(state, player)
#        v = -infinity
#        for (a, s) in game.successors(state):
#            v = max(v, min_value(s))
#        return v
#
#    def min_value(state):
#        if game.terminal_test(state):
#            return game.utility(state, player)
#        v = infinity
#        for (a, s) in game.successors(state):
#            v = min(v, max_value(s))
#        return v
#
#    # Body of minimax_decision starts here:
#    action, state = argmax(game.successors(state),
#                           lambda ((a, s)): min_value(s))
#    return action
