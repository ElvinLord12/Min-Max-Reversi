# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy
import numpy as np
import hashlib

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

        maxscore = -1

        for move in board.calc_valid_moves(self.symbol):
            boardcopy = copy.deepcopy(board)
            boardcopy.make_move(self.symbol, move)
            score = boardcopy.calc_scores()[self.symbol]

            if score > maxscore:
                greedymove = move
                maxscore = score

        return greedymove


class MiniMaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        values = []
        moves = board.calc_valid_moves(self.symbol)
        for move in moves:
            cp = copy.deepcopy(board)
            cp.make_move(self.symbol, move)
            values.append(mini_max(cp, self.symbol, 1))

        return moves[values.index(max(values))]


def mini_max(board, symbol, depth):

    moves = board.calc_valid_moves(symbol)

    if not moves:
        if board.game_continues():
            return mini_max(board, get_opponent_symbol(symbol), depth + 1)
        else:
            scores = board.calc_scores()
            return scores[symbol] - scores[get_opponent_symbol(symbol)]

    else:

        values = []
        for move in moves:
            cp = copy.deepcopy(board)
            cp.make_move(symbol, move)

            values.append(mini_max(cp, get_opponent_symbol(symbol), depth + 1))

        if depth % 2 == 0:
            return max(values)

        else:
            return min(values)


class TransposeMiniMaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):

        #get a list of the unique moves
        moves = calc_unique_moves(board, self.symbol)
        values = []

        #if there's only one move, do that
        if len(moves) == 1:
            return moves[0]

        #for each move
        for move in moves:

            #get a boardstate after each move
            cp = copy.deepcopy(board)
            cp.make_move(self.symbol, move)

            #get the value of that move
            values.append(transpose_mini_max(cp, self.symbol, 1))

        #get the move at the max value
        return moves[values.index(max(values))]


def transpose_mini_max(board, symbol, depth):

    moves = calc_unique_moves(board, symbol)

    #if you have no moves
    if not moves:

        #if the game isn't over
        if board.game_continues():

            #switch to opponent's turn
            return transpose_mini_max(board, get_opponent_symbol(symbol), depth + 1)

        #if the game is over
        else:

            #calculate and return the end score
            scores = board.calc_scores()
            return scores[symbol] - scores[get_opponent_symbol(symbol)]

    #if you have moves:
    else:

        values = []

        #for each move
        for move in moves:

            #make a board for each move
            cp = copy.deepcopy(board)
            cp.make_move(symbol, move)

            #recursive call for each move
            values.append(transpose_mini_max(cp, get_opponent_symbol(symbol), depth + 1))

        #if it was your turn, pick the best move for you
        if depth % 2 == 0:
            return max(values)

        #if it was the opponent turn, pick worst move for you (best for them)
        else:
            return min(values)


def calc_unique_moves(board, symbol):
    u_moves = []
    hashes = set()
    moves = board.calc_valid_moves(symbol)

    for move in moves:
        cp = copy.deepcopy(board)
        cp.make_move(symbol, move)
        board_hash = _hash_set(board)

        if not hashes & board_hash:
            hashes |= board_hash
            u_moves.append(move)

    return u_moves


def _hash_set(board):

    #get the board in an array
    arr_board = _get_arr_board(board)
    h_set = set()

    #for each rotation
    for i in range(4):
        arr_board = np.rot90(arr_board)
        arr_string = str(arr_board)
        arr_hash = hashlib.md5(arr_string.encode())
        h_set.add(arr_hash)

    #mirror the board with transpose
    arr_board = arr_board.T

    #for each mirrored rotation
    for i in range(4):

        #rotate the board 90 degrees
        arr_board = np.rot90(arr_board)

        #convert it to a string
        arr_string = str(arr_board)

        #encode the string and get the md5 hash (string)
        arr_hash = hashlib.md5(arr_string.encode())

        #add the hash to the set (sets can only have unique elements)
        h_set.add(arr_hash)

    #return the set of all the hashes of the board (len <=8)
    return h_set


def _get_arr_board(board):
    #grab the size of the board
    size = board.get_size()

    #make an array
    arr_board = np.zeros((size, size))

    #going through every
    for x in range(size):
        for y in range(size):
            symbol = board.get_symbol_for_position([x, y])

            if symbol == 'X':
                arr_board[x, y] = 1
            if symbol == 'O':
                arr_board[x, y] = -1

    return arr_board


def get_opponent_symbol(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'
