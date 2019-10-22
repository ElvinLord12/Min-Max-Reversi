import random
import copy
import numpy as np
import hashlib

depth_threshold = 4


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

            #calculate and return the end score
            return _get_board_score(board, symbol)

    elif len(moves) == 1:
        board.make_move(symbol, moves[0])
        return mini_max(board, get_opponent_symbol(symbol), depth + 1)

    #if you have moves:
    else:

        if depth < depth_threshold:

            values = []

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
