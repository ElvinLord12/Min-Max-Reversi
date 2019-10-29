from reversi.player5.reversi_players import MiniMaxComputerPlayer, MinMaxPlayerCorner, MiniMaxPlayerWithABPruning, MiniMaxComputerPlayerGreedyMove
import time
import copy

depth_threshold = 3
corners = {(0,0),(0,7),(7,0),(7,7)}
edges = {(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(2,0),(2,1),(2,2),(2,3),(2,4),(2, 5),(2, 6),(2, 7),(3, 0),(3, 1),(3, 2),(3, 3),(3, 4),(3, 5),(3, 6),(3, 7),(4, 0),(4, 1),(4, 2),(4, 3),(4, 4),(4, 5),(4, 6),(4, 7),(5, 0),(5, 1),(5, 2),(5, 3),(5, 4),(5, 5),(5, 6),(5, 7),(6, 0),(6, 1),(6, 2),(6, 3),(6, 4),(6, 5),(6, 6),(6, 7),(7, 1),(7, 2),(7, 3),(7, 4),(7, 5),(7, 6)}


def get_default_player(symbol):
    """
    :returns: a default minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayer


def get_player_a(symbol):
    """
    :author: Milo Rue
    :enchancement: Favors corners and randomizes choice when multiple choices would have the same value
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MinMaxPlayerCorner


def get_player_b(symbol):
    """
    :author: Justin Moczynski
    :enchancement: Some pruning of choices but doesn't actually perform true AB Pruning, simply removes certain choices to cut down on time.
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxPlayerWithABPruning


def get_player_c(symbol):
    """
    :author: Gabe Pesco
    :enchancement: Reorders the move list and attempts best moves earlier to prune more effectively.
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    return MiniMaxComputerPlayerGreedyMove


def get_player_d(symbol):
    """
    :author:
    :enchancement:
    :returns: an enhanced minimax player that can operate successfully on a given 8x8 board
    """
    pass


def get_combined_player(symbol):
    """
    :returns: the best combination of the minimax enhancements that your team can create
    """
    return AlphaBetaPlayer(symbol)


class AlphaBetaPlayer:

    def __init__(self, symbol):
        self.symbol = symbol

    def get_move(self, board):

        #get initial variables for get_move
        start = time.time()
        symbol = self.symbol
        opp_sym = get_opponent_symbol(symbol)
        moves = board.calc_valid_moves(symbol)

        #if we only have one move do that
        if len(moves) == 1:
            return moves[0]

        moves = reorder_moves(moves)
        best_score = -1000
        best_move = moves[0]

        #for move in moves:
        for move in moves:

            mini_max_timer = time.time()

            copy_board = copy.deepcopy(board)
            copy_board.make_move(symbol, move)
            move_score = min_max(copy_board, opp_sym, 1, -1000, 1000)

            if move_score > best_score:
                best_move = move
                best_score = move_score

            end_time = time.time()

            #if the current time elapsed plus how long the next move could take would be beyond our cutoff, return
            if (end_time - start) + (1.35 * (end_time - mini_max_timer)) > 2.5:
                if time.time() - start > 2.7:
                    pass
                return best_move
        if time.time() - start > 2.7:
            print("move skipped! timed out!")
        return best_move


def min_max(board, symbol, depth, alpha, beta):
    if depth % 2 == 0:
        is_max_player = True
    else:
        is_max_player = False

    moves = board.calc_valid_moves(symbol)
    opp_sym = get_opponent_symbol(symbol)

    if not moves:
        if board.game_continues():
            return min_max(board, opp_sym, depth + 1, alpha, beta)
        else:
            if is_max_player:
                return _get_board_score(board, symbol)
            else:
                return _get_board_score(board, opp_sym)

    if len(moves) == 1:
        board.make_move(symbol, moves[0])
        return min_max(board, opp_sym, depth + 1, alpha, beta)

    moves = reorder_moves(moves)

    if depth > depth_threshold:
        board.make_move(symbol, moves[0])

        if is_max_player:
            return _get_board_score(board, symbol)
        else:
            return _get_board_score(board, opp_sym)

    if is_max_player:

        best_value = -1000

        for move in moves:
            copy_board = copy.deepcopy(board)
            copy_board.make_move(symbol, move)

            value = min_max(copy_board, opp_sym, depth + 1, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if beta <= alpha:
                break
        return best_value

    else:

        best_value = 1000

        for move in moves:
            copy_board = copy.deepcopy(board)
            copy_board.make_move(symbol, move)

            value = min_max(copy_board, opp_sym, depth + 1, alpha, beta)
            best_value = min(best_value, value)
            beta = min(beta, best_value)

            if beta <= alpha:
                break
        return best_value

def _get_board_score(board, symbol):
    scores = board.calc_scores()
    return scores[symbol] - scores[get_opponent_symbol(symbol)]

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

def get_opponent_symbol(symbol):
    #returns the opponent symbol, assumes X and O are only chars being used
    if symbol == 'X':
        return 'O'
    else:
        return 'X'
