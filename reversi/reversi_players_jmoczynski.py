# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
import math


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
            move = input(self.symbol + ', enter your move (x,y):').lower()
            move_list = move.split(",")
            move = move_list
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

    def get_name(self):
        return str(type(self).__name__)


class RandomComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        return random.choice(board.calc_valid_moves(self.symbol))

    def get_name(self):
        return str(type(self).__name__)

class GreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        moves_scores = list()
        for potential_move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, potential_move)
            moves_scores.append(board_copy.calc_scores()[self.symbol])
        return moves[moves_scores.index(max(moves_scores))]

    def get_name(self):
        return str(type(self).__name__)

class UnGreedyComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        moves_scores = list()
        for potential_move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, potential_move)
            moves_scores.append(board_copy.calc_scores()[self.symbol])
        return moves[moves_scores.index(min(moves_scores))]

    def get_name(self):
        return str(type(self).__name__)





class MiniMaxPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def mini_max(self, board, symbol, depth):
        moves = board.calc_valid_moves(symbol)
        if not moves:
            if board.game_continues():
                return self.mini_max(board, board.get_opponent_symbol(symbol), depth + 1)
            else:
                scores = board.calc_scores()
                return scores[symbol]-scores[board.get_opponent_symbol(symbol)]
        else:
            values = []
            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(symbol, move)
                values.append(self.mini_max(board_copy, board_copy.get_opponent_symbol(symbol), depth + 1))
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
            values.append(self.mini_max(board_copy, self.symbol, 1))
        return moves[values.index(max(values))]

    def get_name(self):
        return str(type(self).__name__)

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

class MiniMaxPlayerWithABPruning:

    def __init__(self, symbol):
        self.symbol = symbol

    def mini_max_with_ab_pruning(self, board, symbol, depth, alpha, beta):
        moves = board.calc_valid_moves(symbol)
        if not moves:
            if board.game_continues():
                return self.mini_max_with_ab_pruning(board, board.get_opponent_symbol(symbol), depth + 1, alpha, beta)
            else:
                scores = board.calc_scores()
                return scores[symbol] - scores[board.get_opponent_symbol(symbol)]
        else:
            values = []
            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(symbol, move)
                values.append(self.mini_max_with_ab_pruning(board_copy, board_copy.get_opponent_symbol(symbol), depth + 1, alpha, beta))
                for value in values:
                    if value > beta:
                        break
                    elif value < alpha:
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
            values.append(self.mini_max_with_ab_pruning(board_copy, self.symbol, 1, -math.inf, math.inf))
        return moves[values.index(max(values))]

    def get_name(self):
        return str(type(self).__name__)