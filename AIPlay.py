from connect_four import Game
from connect_four import NONE, RED, YELLOW
import random
from connect_four_eval import BoardEvaluation
from minimax import minimax_decision
from cross_mutate import sbx, pm


def play(games, win, player1, player2):
    player1_wins = 0
    player2_wins = 0
    ties = 0
    last_winner = -1
    num_games = 1

    while player1_wins < win and player2_wins < win and num_games < games:
        g = Game(7, 6, 4)
        turns_played = 0
        if last_winner == -1:
            turn = random.randint(1,2)
        else:
            turn = last_winner # winner gets to go first

        while g.get_winner() is None and turns_played < g.rows * g.cols - 1:
            if turn == YELLOW:
                next_move = minimax_decision(g,YELLOW,player2)
                g.insert(next_move, turn)
            else:
                next_move = minimax_decision(g,RED,player1)
                g.insert(next_move, turn)

            # time.sleep(0.1)
            turns_played += 1
            # g.print_board()
            turn = YELLOW if turn == RED else RED

        num_games += 1
        winner = g.get_winner()
        last_winner = winner
        if winner == 1:
            player1_wins += 1
        elif winner == 2:
            player2_wins += 1
        else:
            ties += 1

    return [player1_wins, player2_wins, ties]


def one_round(player_list, num_games, best):
    winners = list()
    random.shuffle(player_list)
    for i in range(0, len(player_list)-1, 2):
        [win1, win2, ties] = play(num_games, best, player_list[i], player_list[i+1])
        if win1 > win2:
            winners.append(player_list[i])
        elif win2 > win1:
            winners.append(player_list[i+1])
        else:
            r = random.sample([i, i+1], 1)
            winners.append(player_list[r[0]])
    return winners


def tournament(player_list, rounds, num_games, best):
    for i in range(rounds):
        random.shuffle(player_list)
        winners = one_round(player_list, num_games, best)
        player_list = winners
    return winners

if __name__ == '__main__':
    players = list()
    num_players = 64
    num_generation = 100

    # initialize the players
    for i in range(num_players):
        my_cluster1 = random.randrange(100)
        my_cluster2 = random.randrange(100)
        my_cluster3 = random.randrange(100)
        my_cluster4 = random.randrange(100)
        my_free_space_mult = random.randrange(10)
        my_free_space_exp = random.randrange(10)
        your_cluster1 = -random.randrange(100)
        your_cluster2 = -random.randrange(100)
        your_cluster3 = -random.randrange(100)
        your_cluster4 = -random.randrange(100)
        your_free_space_mult = -random.randrange(10)
        your_free_space_exp = random.randrange(10)
        players.append(
            BoardEvaluation([my_cluster1, my_cluster2, my_cluster3, my_cluster4, my_free_space_mult, my_free_space_exp,
                            your_cluster1, your_cluster2, your_cluster3, your_cluster4, your_free_space_mult,
                            your_free_space_exp]))

    for i in range(num_generation):
        winners = tournament(players, 1, 11, 6)
        players = winners
        print("generation: ", i)
        for winner in winners:
            print(str(winner))

        # cross winner variables
        for j in range(0, len(winners) - 1, 2):
            [child1, child2] = sbx(winners[j].eval_vector, winners[j+1].eval_vector, 20, -100, 100)
            mutated_child1 = pm(child1, 20, -100, 100, 1/len(child1))
            mutated_child2 = pm(child2, 20, -100, 100, 1 / len(child2))
            players.append(BoardEvaluation(mutated_child1))
            players.append(BoardEvaluation(mutated_child2))
