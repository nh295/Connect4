from connect_four import Game
from connect_four import NONE, RED, YELLOW
import random
from connect_four_eval import BoardEvaluation
from minimax import minimax_decision


def play(games, win, ai):
    player1_wins = 0
    player2_wins = 0
    ties = 0
    last_winner = -1
    num_games = 1

    while player1_wins < win and player2_wins < win and num_games <= games:
        g = Game(7, 6, 4)
        turns_played = 0
        if last_winner == -1:
            turn = random.randint(1,2)
        else:
            turn = last_winner # winner gets to go first

        while g.get_winner() is None and turns_played < g.rows * g.cols - 1:
            if turn == YELLOW:
                next_move = minimax_decision(g,YELLOW,ai)
                g.insert(next_move, turn)
            else:
                g.print_board()
                next_move = input('{}\'s turn: '.format('Red' if turn == RED else 'Yellow'))
                g.insert(int(next_move), turn)

            # time.sleep(0.1)
            turns_played += 1
            # g.print_board()
            turn = YELLOW if turn == RED else RED

        num_games += 1
        winner = g.get_winner()
        if winner == 1:
            player1_wins += 1
        elif winner == 2:
            player2_wins += 1
        else:
            ties += 1

    return [player1_wins, player2_wins, ties]


if __name__ == '__main__':
    [wins, losses, ties] = play(3, 2, BoardEvaluation([-72.81, -15.77, 064.15, 011.97, 030.46, 013.75, 090.68, 017.08, -99.65, -14.23, -68.97, -15.85]))
    print('Wins: {:d}, Losses: {:d}, Ties:{:d}'.format(wins, losses, ties))