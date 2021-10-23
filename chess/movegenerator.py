from chess.constants import DEAD_SQUARES
from chess.pieces.bishop import Bishop
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook


def legal_moves(piece, board):
    """
    Determines whether a move is legal. Current position is known to piece, target is parameter
    :return: list of legal square_nr
    """

    # https://www.chess.com/club/4-player-chess-1 for rules

    result = []

    capture = False  # TODO: in case of capture do something

    sqrnr = piece.get_square()
    if isinstance(piece, Pawn):  # No en passant in 4 player chess

        if piece.get_player() == 'n' and is_inside_board(sqrnr + 14):  # check if player is n and still on board
            result.append(sqrnr + 14)
            if sqrnr < 25:  # check if start position
                result.append(sqrnr + 28)
            if is_inside_board(sqrnr + 13) and is_occupied_by_enemy(piece, sqrnr + 13, board):
                result.append(sqrnr + 13)
            if is_inside_board(sqrnr + 15) and is_occupied_by_enemy(piece, sqrnr + 15, board):
                result.append(sqrnr + 15)

        if piece.get_player() == 's' and is_inside_board(sqrnr - 14):
            result.append(sqrnr - 14)
            if sqrnr > 170:  # check if start position
                result.append(sqrnr - 28)
            if is_inside_board(sqrnr - 13) and is_occupied_by_enemy(piece, sqrnr - 13, board):
                result.append(sqrnr - 13)
            if is_inside_board(sqrnr - 15) and is_occupied_by_enemy(piece, sqrnr - 15, board):
                result.append(sqrnr - 15)

        if piece.get_player() == 'w' and is_inside_board(sqrnr + 1):
            result.append(sqrnr + 1)
            if sqrnr in [43, 57, 71, 85, 99, 113, 127, 141]:  # check if start position
                result.append(sqrnr + 2)
            if is_inside_board(sqrnr - 13) and is_occupied_by_enemy(piece, sqrnr - 13, board):
                result.append(sqrnr - 13)
            if is_inside_board(sqrnr + 15) and is_occupied_by_enemy(piece, sqrnr + 15, board):
                result.append(sqrnr + 15)

        if piece.get_player() == 'e' and is_inside_board(sqrnr - 1):
            result.append(sqrnr - 1)
            if sqrnr in [54, 68, 82, 96, 110, 124, 138, 152]:  # check if start position
                result.append(sqrnr - 2)
            if is_inside_board(sqrnr + 13) and is_occupied_by_enemy(piece, sqrnr + 13, board):
                result.append(sqrnr + 13)
            if is_inside_board(sqrnr - 15) and is_occupied_by_enemy(piece, sqrnr - 15, board):
                result.append(sqrnr - 15)

    elif isinstance(piece, Rook):
        offset = [-1, 1, -14, 14]
        result = sliding_piece(offset, sqrnr, piece, board)

    elif isinstance(piece, Bishop):
        offset = [-13, 13, -15, 15]
        result = sliding_piece(offset, sqrnr, piece, board)

    elif isinstance(piece, Knight):
        offset = [-16, -29, -27, -12, 16, 29, 27, 12]
        for ofs in offset:
            if is_inside_board(sqrnr + ofs) and \
                    (board.board[sqrnr + ofs] is None or
                     is_occupied_by_enemy(piece, sqrnr + ofs, board)):
                result.append(sqrnr + ofs)


    elif isinstance(piece, King):  # TODO: not allowed to walk into check
        offset = [-13, -14, -15, -1, 1, 13, 14, 15]
        for ofs in offset:
            if is_inside_board(sqrnr + ofs) and \
                    (board.board[sqrnr + ofs] is None or
                     is_occupied_by_enemy(piece, sqrnr + ofs, board)):
                result.append(sqrnr + ofs)

    elif isinstance(piece, Queen):
        offset = [-13, 13, -15, 15, -1, 1, -14, 14]
        result = sliding_piece(offset, sqrnr, piece, board)

    return result


def is_occupied_by_enemy(piece, square_nr, board):
    if board.board[square_nr] is None:
        return False
    else:
        return piece.get_player() != board.board[square_nr].get_player()


def is_inside_board(square_nr):
    return 2 < square_nr < 193 and square_nr not in DEAD_SQUARES


def sliding_piece(offset, sqrnr, piece, board):
    result = []

    for ofs in offset:
        temp_sqrnr = sqrnr
        while is_inside_board(temp_sqrnr + ofs) and \
                (board.board[temp_sqrnr + ofs] is None or
                 is_occupied_by_enemy(piece, temp_sqrnr + ofs, board)):
            result.append(temp_sqrnr + ofs)
            if is_occupied_by_enemy(piece, temp_sqrnr + ofs, board):
                capture = True  # TODO: probably give target square parameter?!
                break
            temp_sqrnr += ofs
    return result
