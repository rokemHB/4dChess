from chess.constants import DEAD_SQUARES
from chess.pieces.bishop import Bishop
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook


def is_legal_move(piece, target_square):
    """
    Determines whether a move is legal. Current position is known to piece, target is parameter
    :return: list of legal square_nr
    """

    # TARGET EVEN NECESSARY?? MAYBE JUST GIVE LIST OF LEGAL MOVES AND TEST IF TARGET %in% LIST

    result = []

    sqrnr = piece.get_square()
    if isinstance(piece, Pawn):
        if piece.get_player() == 'n' and is_inside_board(sqrnr + 14):  # check if player is n and still on board
            result.append(sqrnr + 14)
            if sqrnr < 25:  # check if start position
                result.append(sqrnr + 28)
            if is_inside_board(sqrnr + 13) and is_occupied_by_enemy(sqrnr + 13):
                result.append(sqrnr + 13)
            if is_inside_board(sqrnr + 15) and is_occupied_by_enemy(sqrnr + 15):
                result.append(sqrnr + 15)


    elif isinstance(piece, Rook):
        pass
    elif isinstance(piece, Knight):
        pass
    elif isinstance(piece, Bishop):
        pass
    elif isinstance(piece, King):
        pass
    elif isinstance(piece, Queen):
        pass
    return result


def is_occupied_by_enemy(square_nr):
    pass

def is_inside_board(square_nr):
    return 2 < square_nr < 193 and square_nr not in DEAD_SQUARES