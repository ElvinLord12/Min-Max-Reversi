# adapted by Toby Dragon from original source code by Al Sweigart, available with creative commons license: https://inventwithpython.com/#donate
import random
import copy

depth_threshold = 3


class HumanPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        # Let the player type in their move.
        # Returns the move as [x, y] (or returns the strings 'hints' or 'quit')
        valid_digits = []
        for i in range(1, board.get_size() + 1):
            valid_digits.append(str(i))
        no_valid_move = True
        while no_valid_move:
            move = input(self.symbol + ', enter your move:').lower()
            if len(move) == 2 and move[0] in valid_digits and move[1] in valid_digits:
                x = int(move[0]) - 1
                y = int(move[1]) - 1
                if board.is_valid_move(self.symbol, (x, y)):
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


class GreedyAgent:
    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        max = 0
        for move in moves:
            greedy = len(board.is_valid_move(self.symbol, move))
            if greedy > max:
                max = greedy
                damove = move
        return damove


class MinMaxPlayerQ:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):
        moves = board.calc_valid_moves(self.symbol)
        values = []

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
            return _get_board_score(board, symbol)

    else:

        heuristicval = heuristic(symbol, board)
        if heuristicval < 30:

            values = []

            for move in moves:
                board_copy = copy.deepcopy(board)
                board_copy.make_move(symbol, move)
                values.append(mini_max(board_copy, get_opponent_symbol(symbol), depth + 1))

            if depth % 2 == 0:
                return max(values)

            else:
                return min(values)

        else:
            return _get_board_score(board, symbol)


def _get_board_score(board, symbol):
    scores = board.calc_scores()
    return scores[symbol] - scores[get_opponent_symbol(symbol)]


def get_opponent_symbol(symbol):
    if symbol == 'X':
        return 'O'
    else:
        return 'X'


def heuristic(symbol, board):
    val = 100 * (len(board.calc_valid_moves(symbol)) - len(board.calc_valid_moves(get_opponent_symbol(symbol)))) / (
        len((board.calc_valid_moves(symbol))) + len(board.calc_valid_moves(get_opponent_symbol(symbol))))

    return abs(val)
