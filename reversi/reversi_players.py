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

        max_score = -1

        for move in board.calc_valid_moves(self.symbol):
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, move)
            score = board_copy.calc_scores()[self.symbol]

            if score > max_score:
                greedy_move = move
                max_score = score

        return greedy_move

#ignore this class and the mini_max function, as we already use the transposition table version
class MiniMaxComputerPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        values = []
        moves = board.calc_valid_moves(self.symbol)
        for move in moves:
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, move)
            values.append(mini_max(board_copy, self.symbol, 1))

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
            board_copy = copy.deepcopy(board)
            board_copy.make_move(symbol, move)

            values.append(mini_max(board_copy, get_opponent_symbol(symbol), depth + 1))

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

        for move in moves:

            #get a board state after the move
            board_copy = copy.deepcopy(board)
            board_copy.make_move(self.symbol, move)

            #get the value of that move
            values.append(transpose_mini_max(board_copy, self.symbol, 1))

        #get the move at the index of the max value
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
            board_copy = copy.deepcopy(board)
            board_copy.make_move(symbol, move)

            #recursive call for each move
            values.append(transpose_mini_max(board_copy, get_opponent_symbol(symbol), depth + 1))

        #if it was your turn, pick the best move for you
        if depth % 2 == 0:
            return max(values)

        #if it was the opponent turn, pick worst move for you (best for them)
        else:
            return min(values)


def calc_unique_moves(board, symbol):

    u_moves = []
    hashes = set()

    #grab the valid moves
    moves = board.calc_valid_moves(symbol)

    #for each move
    for move in moves:

        #make a copy board and do a move
        cp = copy.deepcopy(board)
        cp.make_move(symbol, move)

        #get the set of hashes of that board state
        board_hash = _hash_set(board)

        #if there are no hashes in common with the set of hashes, it is a unique move
        if not hashes & board_hash:

            #add that board's hashes to the set of hashes
            hashes |= board_hash

            #add it to unique moves
            u_moves.append(move)

    return u_moves


def _rotation_hashes(board):

    #grab an empty set
    r_set = set()

    #for each of the 4 rotations
    for i in range(4):

        #rotate by 90 degrees
        board = np.rot90(board)

        #convert board to a string, add the md5 hash to the set (hashes already in the set are not added)
        r_set.add(hashlib.md5(str(board).encode()))

    return r_set


def _hash_set(board):

    #get the board in an array
    arr_board = _get_arr_board(board)

    #combine the rotation hashes of the array and the array transposed
    return _rotation_hashes(arr_board) | _rotation_hashes(arr_board.T)


def _get_arr_board(board):
    #grab the size of the board
    size = board.get_size()

    #make an array
    arr_board = np.zeros((size, size))

    #going through every tile
    for x in range(size):
        for y in range(size):

            #grab the symbol
            symbol = board.get_symbol_for_position([x, y])

            #put in values for each symbol
            if symbol == 'X':
                arr_board[x, y] = 1
            if symbol == 'O':
                arr_board[x, y] = -1

            #leave empty tiles as zeros

    return arr_board


def get_opponent_symbol(symbol):
    #returns the opponent symbol, assumes X and O are only chars being used
    if symbol == 'X':
        return 'O'
    else:
        return 'X'
