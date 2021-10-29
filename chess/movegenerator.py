import copy

from chess.constants import DEAD_SQUARES, SQUARE_SIZE
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

# start locations pawns of players w and e
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

            # make sure we can not jump from left to right side by comparing x coordinates
            if abs(board.get_coordinates_from_square_nr(sqrnr)[0] -
                   board.get_coordinates_from_square_nr(sqrnr + ofs)[0]) > (2 * SQUARE_SIZE):
                continue

            if is_inside_board(sqrnr + ofs) and \
                    (board.board[sqrnr + ofs] is None or
                     is_occupied_by_enemy(piece, sqrnr + ofs, board)):
                result.append(sqrnr + ofs)

    elif isinstance(piece, King):  # TODO: How to give points when someone sets check? Because now we only try when it's respective players turn
        offset = [-13, -14, -15, -1, 1, 13, 14, 15]
        for ofs in offset:

            # make sure we can not jump from left to right side by comparing x coordinates
            if abs(board.get_coordinates_from_square_nr(sqrnr)[0] -
                   board.get_coordinates_from_square_nr(sqrnr + ofs)[0]) > (3 * SQUARE_SIZE):
                continue

            if is_inside_board(sqrnr + ofs) and \
                    (board.board[sqrnr + ofs] is None or
                     is_occupied_by_enemy(piece, sqrnr + ofs, board)):

                """
                ### Make sure king does not walk into check.
                ### Makes copy of board, sets king at each possible position and 
                ###     tests with check_checker if king is in check.
                """
                test_board = copy.deepcopy(board)  # TODO: too many copies .... performance prolly bad. Any better way?
                new_pos = piece.get_square() + ofs
                player = piece.get_player()
                test_board.set_piece(new_pos, King(new_pos, player))
                test_board.set_piece(piece.get_square(), None)
                test_board.king_pos[player] = new_pos

                if not check_checker(piece.get_player(), test_board):
                    result.append(sqrnr + ofs)

    elif isinstance(piece, Queen):
        offset = [-13, 13, -15, 15, -1, 1, -14, 14]
        result = sliding_piece(offset, sqrnr, piece, board)

    return result


def is_occupied_by_enemy(piece, square_nr, board):
    """
    Returns true when a given square is occupied by an enemy for given player
    """
    if board.board[square_nr] is None:
        return False
    else:
        return piece.get_player() != board.board[square_nr].get_player()


def is_inside_board(square_nr):
    """
    checks whether a given square number is within board limits
    """
    return 2 < square_nr < 193 and square_nr not in DEAD_SQUARES


def sliding_piece(offset, sqrnr, piece, board):
    """
    Takes care of the logic for all sliding pieces
    :param offset: directions to check, rook vs bishop vs both
    :param sqrnr: square number to start from
    :param piece: piece for which evaluation shell be done
    :param board: board on which respective game takes place
    :return: int array of square numbers indicating legal moves to go for given piece
    """
    result = []

    for ofs in offset:
        temp_sqrnr = sqrnr

        while is_inside_board(temp_sqrnr + ofs) and \
                (board.board[temp_sqrnr + ofs] is None or
                 is_occupied_by_enemy(piece, temp_sqrnr + ofs, board)):

            step_counter = 0

            # make sure we can not jump from left to right side by comparing x coordinates
            if abs(board.get_coordinates_from_square_nr(temp_sqrnr)[0] -
                   board.get_coordinates_from_square_nr(temp_sqrnr + ofs)[0]) > (2 * SQUARE_SIZE):
                break
            ####### Really bad performance, might look for different implementation
            if step_counter < 1:
                test_board = copy.deepcopy(board)  # TODO: too many copies .... performance prolly bad. Any better way?
                new_pos = piece.get_square() + ofs
                player = piece.get_player()
                if isinstance(piece, Rook):
                    test_board.set_piece(new_pos, Rook(new_pos, player))
                elif isinstance(piece, Bishop):
                    test_board.set_piece(new_pos, Bishop(new_pos, player))
                elif isinstance(piece, Queen):
                    test_board.set_piece(new_pos, Queen(new_pos, player))

                test_board.set_piece(piece.get_square(), None)
                #test_board.king_pos[player] = new_pos   # nur wichtig wenn King bewegt wird

                #if not check_checker(piece.get_player(), test_board):
                result.append(temp_sqrnr + ofs)
            else:
                result.append(temp_sqrnr + ofs)
            #######
            #result.append(temp_sqrnr + ofs)
            if is_occupied_by_enemy(piece, temp_sqrnr + ofs, board):
                capture = True  # TODO: probably give target square parameter?!
                break
            step_counter += 1
            temp_sqrnr += ofs
    return result


def check_checker(player, board):
    """
    Test whether a player is checked. Looks up king position in board.king_pos dict.
    :param player: player for which the check should be checked
    :param board: board of the given game
    :return: True if player is in check
    """
    #test_board = copy.deepcopy(board)
    test_board = board
    pos = test_board.king_pos.get(player)

    # set new pieces to position where King is for respective player
    # Queen
    test_board.set_piece(pos, Queen(pos, player))
    result = legal_moves(test_board.get_piece(pos), test_board)
    for res in result:
        if isinstance(test_board.get_piece(res), Queen) and test_board.get_piece(res).get_player() != player:
            return True

    # Bishop
    test_board.set_piece(pos, Bishop(pos, player))
    result = legal_moves(test_board.get_piece(pos), test_board)
    for res in result:
        if isinstance(test_board.get_piece(res), Bishop) and test_board.get_piece(res).get_player() != player:
            return True

    # Rook
    test_board.set_piece(pos, Rook(pos, player))
    result = legal_moves(test_board.get_piece(pos), test_board)
    for res in result:
        if isinstance(test_board.get_piece(res), Rook) and test_board.get_piece(res).get_player() != player:
            return True

    # Knight
    test_board.set_piece(pos, Knight(pos, player))
    result = legal_moves(test_board.get_piece(pos), test_board)
    for res in result:
        if isinstance(test_board.get_piece(res), Knight) and test_board.get_piece(res).get_player() != player:
            return True

    # King
    sqrnr = board.king_pos.get(player)
    for dir in directions:
        if abs(board.get_coordinates_from_square_nr(sqrnr)[0] -
               board.get_coordinates_from_square_nr(sqrnr + dir)[0]) > (2 * SQUARE_SIZE):
            continue

        if is_inside_board(sqrnr + dir):
            if isinstance(test_board.get_piece(sqrnr + dir), King) and \
                    test_board.get_piece(sqrnr + dir).get_player() != player:
                return True

    # Pawn
    if player == 'n':
        temp_piece = test_board.get_piece(pos + 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['s', 'w']:
                return True
        temp_piece = test_board.get_piece(pos + 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['s', 'e']:
                return True
        temp_piece = test_board.get_piece(pos - 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 'e':
                return True
        temp_piece = test_board.get_piece(pos - 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 'w':
                return True

    elif player == 's':
        temp_piece = test_board.get_piece(pos + 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 'w':
                return True
        temp_piece = test_board.get_piece(pos + 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 'e':
                return True
        temp_piece = test_board.get_piece(pos - 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['e', 'n']:
                return True
        temp_piece = test_board.get_piece(pos - 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['w', 'n']:
                return True

    elif player == 'w':
        temp_piece = test_board.get_piece(pos + 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 's':
                return True
        temp_piece = test_board.get_piece(pos + 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['s', 'e']:
                return True
        temp_piece = test_board.get_piece(pos - 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['e', 'n']:
                return True
        temp_piece = test_board.get_piece(pos - 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 'n':
                return True

    elif player == 'e':
        temp_piece = test_board.get_piece(pos + 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['s', 'w']:
                return True
        temp_piece = test_board.get_piece(pos + 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 's':
                return True
        temp_piece = test_board.get_piece(pos - 13)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() == 'n':
                return True
        temp_piece = test_board.get_piece(pos - 15)
        if isinstance(temp_piece, Pawn):
            if temp_piece.get_player() in ['n', 'w']:
                return True

    return False
