from chess.constants import DEAD_SQUARES
from chess.pieces.bishop import Bishop
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook


# position offsets for north, northeast ...
n = -14
ne = -13
e = 1
se = 15
s = 14
sw = 13
w = -1
nw = -15
directions = [n, ne, e, se, s, sw, w, nw]

# start locations for players w and e
w_start = [43, 57, 71, 85, 99, 113, 127, 141]
e_start = [54, 68, 82, 96, 110, 124, 138, 152]


def legal_moves(piece, board):
    """
    Determines whether a move is legal. Current position is known to piece
    :return: list of legal square_nr
    """

    # https://www.chess.com/club/4-player-chess-1 for rules

    result = []

    capture = False  # TODO: in case of capture do something

    if piece is None:
        return
    else:
        sqrnr = piece.get_square()
    if isinstance(piece, Pawn):  # No en passant in 4 player chess

        if piece.get_player() == 'n':
            player_direction = 4
        elif piece.get_player() == 's':
            player_direction = 0
        elif piece.get_player() == 'w':
            player_direction = 2
        else:
            player_direction = 6

        if not is_inside_board(sqrnr + directions[player_direction]):
            return result
        if not is_occupied_by_enemy(piece, sqrnr + directions[player_direction], board):
            result.append(sqrnr + directions[player_direction])
            if (player_direction == 4 and sqrnr < 25) or \
                    (player_direction == 0 and sqrnr > 170) or \
                    (player_direction == 2 and sqrnr in w_start) or \
                    (player_direction == 6 and sqrnr in e_start):
                result.append(sqrnr + 2 * directions[player_direction])
        if is_inside_board(sqrnr + directions[(player_direction - 1) % 8]) and \
                is_occupied_by_enemy(piece, sqrnr + directions[(player_direction - 1) % 8], board):
            result.append(sqrnr + directions[(player_direction - 1) % 8])
        if is_inside_board(sqrnr + directions[(player_direction + 1) % 8]) and \
                is_occupied_by_enemy(piece, sqrnr + directions[(player_direction + 1) % 8], board):
            result.append(sqrnr + directions[(player_direction + 1) % 8])

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


    # TODO: SET KING_X POSITION IN BOARD.KING_N etc
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

def check_checker(piece, board):
    pass
