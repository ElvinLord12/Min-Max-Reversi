import random
import copy
import numpy as np
import hashlib
import math

depth_threshold = 3
corners = {(0,0),(0,7),(7,0),(7,7)}
edges = {(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(2,0),(2,1),(2,2),(2,3),(2,4),(2, 5),(2, 6),(2, 7),(3, 0),(3, 1),(3, 2),(3, 3),(3, 4),(3, 5),(3, 6),(3, 7),(4, 0),(4, 1),(4, 2),(4, 3),(4, 4),(4, 5),(4, 6),(4, 7),(5, 0),(5, 1),(5, 2),(5, 3),(5, 4),(5, 5),(5, 6),(5, 7),(6, 0),(6, 1),(6, 2),(6, 3),(6, 4),(6, 5),(6, 6),(6, 7),(7, 1),(7, 2),(7, 3),(7, 4),(7, 5),(7, 6)}


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size()+1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, ( x, y) ):
                    no_valid_move = False
                    return [x, y]
                else:
                    print('Not a valid move.')
            else:
                print('Bad input. Type valid x digit, then the y digit.')


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))


class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):

        max_score = -99

        for move in board.calc_valid_moves(self.symbol):
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, move)
            score = _get_board_score(board_copy, self.symbol)

            if score > max_score:
                greedy_move = move
                max_score = score

        return greedy_move


class MiniMaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):

        symbol = self.symbol
        #get a list of the unique moves
        moves = board.calc_valid_moves(symbol)
        values = []

        #if there's only one move, do that
        if len(moves) == 1:
            return moves[0]

        moves = reorder_moves(moves)

        for move in moves:

            #get a board state after the move
            board_copy = copy.deepcopy(board)
            board_copy.make_move(symbol, move)

            #get the value of that move
            values.append(mini_max(board_copy, symbol, 0))

        #get the moves at the tied for the max value
        max_value = max(values)
        tied_moves = []
        for i in range(len(values)):
            if values[i] == max_value:
                tied_moves.append(moves[i])

        #return a random one of them
        return random.choice(tied_moves)


class MiniMaxPlayerWithPruning:

    def __init__(self, symbol):
        self.symbol = symbol

    def mini_max_with_pruning(self, board, symbol, depth):
        moves = board.calc_valid_moves(symbol)
        if not moves:
            if board.game_continues():
                return self.mini_max_with_pruning(board, board.get_opponent_symbol(symbol), depth + 1)
            else:
                scores = board.calc_scores()
                return scores[symbol] - scores[board.get_opponent_symbol(symbol)]
        else:
            values = []
            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(symbol, move)
                values.append(self.mini_max_with_pruning(board_copy, board_copy.get_opponent_symbol(symbol), depth + 1))
                max_val = max(values[0:1])
                min_val = min(values[0:1])
                for value in values[2:]:
                    if value > max_val:
                        max_val = value
                        if depth % 2 == 0:
                            break
                    elif value < min_val:
                        min_val = value
                        if depth % 2 != 0:
                            break
                if depth % 2 == 0:
                    return max(values)
                else:
                    return min(values)

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        values = []
        for move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, move)
            values.append(self.mini_max_with_pruning(board_copy, self.symbol, 1))
        return moves[values.index(max(values))]

    def get_name(self):
        return str(type(self).__name__)

def mini_max(board, symbol, depth):

    moves = board.calc_valid_moves(symbol)

    #if you have no moves
    if not moves:

        #if the game isn't over
        if board.game_continues():

            #switch to opponent's turn
            return mini_max(board, get_opponent_symbol(symbol), depth + 1)

        #if the game is over
        else:

            #if its not your turn, get your symbol
            if depth % 2 == 1:
                symbol = get_opponent_symbol(symbol)

            #calculate and return the end score
            return _get_board_score(board, symbol)

    elif len(moves) == 1:
        board.make_move(symbol, moves[0])
        return mini_max(board, get_opponent_symbol(symbol), depth + 1)

    #if you have moves:
    else:

        if depth < depth_threshold:

            values = []

            moves = reorder_moves(moves)

            #for each move
            for move in moves:

                #make a board for each move
                board_copy = copy.deepcopy(board)
                board_copy.make_move(symbol, move)

                #recursive call for each move
                values.append(mini_max(board_copy, get_opponent_symbol(symbol), depth + 1))

            #if it was your turn, pick the best move for you
            if depth % 2 == 0:
                return max(values)

            #if it was the opponent turn, pick worst move for you (best for them)
            else:
                return min(values)

        else:
            if depth % 2 == 1:
                symbol = get_opponent_symbol(symbol)

            return _get_board_score(board, symbol)


def _get_board_score(board, symbol):
    scores = board.calc_scores()
    return scores[symbol] - scores[get_opponent_symbol(symbol)]


def get_opponent_symbol(symbol):
    #returns the opponent symbol, assumes X and O are only chars being used
    if symbol == 'X':
        return 'O'
    else:
        return 'X'


def reorder_moves(moves):
    corner_moves = []
    edge_moves = []
    remaining_moves = []

    for move in moves:
        move_tuple = tuple(move)
        if move_tuple in corners:
            corner_moves.append(move)
        elif move_tuple in edges:
            edge_moves.append(move)
        else:
            remaining_moves.append(move)

    return corner_moves + edge_moves + remaining_moves
