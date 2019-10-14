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

    def min_max(self, board, depth):
        if depth%2 == 0:
            best = [-1,-1,-infinity]
        else:
            best = [-1,-1,+infinity]

        if depth == 0 or not board.game_continues:
            score_dict = board.calc_scores
            score = score_dict.get("X")
            return [-1,-1,score]
        for move in board.calc_valid_moves(self.symbol):
            x, y = move[0], move[1]
            board.make_move(self.symbol, [x,y])
            score = self.min_max(board, depth-1)
            score[0], score[1] = x, y

            if depth % 2 == 0:


    def get_move(self, board):0
0