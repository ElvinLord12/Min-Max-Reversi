# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
from math import inf as infinity


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
        choices = board.calc_valid_moves(self.symbol)

        greed = 0

        for i in choices:
            if len(board.is_valid_move(self.symbol, i)) > greed:
                greed = len(board.is_valid_move(self.symbol, i))
                choice = i

        return choice


class MinMaxPlayer:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        scores = []

        if len(moves) == 1:
            return moves[0]
        for move in moves:
            board_state = copy.deepcopy(board)
            board_state.make_move(self.symbol, move)

            scores.append(self.min_max(board_state, self.symbol, 1))


        return moves[scores.index(max(scores))]

    def min_max(self, board, symbol, depth):

        # all valid moves
        moves = board.calc_valid_moves(symbol)

        if not moves:
            if board.game_continues():
                return self.min_max(board, turn(symbol), depth +1)
            else:
                return _get_board_score(board, symbol)
        else:
            if depth < 3: # depth threshold
                scores = []

                for move in moves:
                    board_state = copy.deepcopy(board)
                    board_state.make_move(symbol, move);

                    scores.append(self.min_max(board_state, turn(symbol), depth + 1))

                # for max player
                if depth % 2 == 0:
                    return max(scores)

                # for min player
                else:
                    return min(scores)

            else:
                return _get_board_score(board, symbol)


class MinMaxPlayerCorner:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        scores = []

        for move in moves:
            if move == [0, 7] or move == [7, 0] or move == [7, 7] or move == [0, 0]:
                return move

        if len(moves) == 1:
            return moves[0]
        for move in moves:
            board_state = copy.deepcopy(board)
            board_state.make_move(self.symbol, move)

            scores.append(self.min_max(board_state, self.symbol, 1))

        return moves[scores.index(max(scores))]

    def min_max(self, board, symbol, depth):

        # all valid moves
        moves = board.calc_valid_moves(symbol)

        if not moves:
            if board.game_continues():
                return self.min_max(board, turn(symbol), depth + 1)
            else:
                return _get_board_score(board, symbol)
        else:
            if depth < 3:  # depth threshold
                scores = []

                for move in moves:
                    board_state = copy.deepcopy(board)
                    board_state.make_move(symbol, move);

                    scores.append(self.min_max(board_state, turn(symbol), depth + 1))

                # for max player
                if depth % 2 == 0:
                    max_score = max(scores)
                    max_choices = []
                    for score in scores:
                        if score == max_score:
                            max_choices.append(score)
                    return random.choice(max_choices)

                # for min player
                else:
                    return min(scores)

            else:
                return _get_board_score(board, symbol)

def turn(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'


def _get_board_score(board, symbol):
    scores = board.calc_scores()
    return scores[symbol] - scores[turn(symbol)]