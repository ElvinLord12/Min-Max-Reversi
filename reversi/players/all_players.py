from reversi.reversi_players import *

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
    pass