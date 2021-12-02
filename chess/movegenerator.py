from chess import piece
from chess.constants import NORTH_INDEX, SOUTH_INDEX
from chess.move import Move
from chess.precalculations import num_squares_to_edge, direction_offsets, knight_attack_bitboards, \
    bitboard_contains_square, pawn_attack_bitboards, king_attack_bitboards, king_moves


class MoveGenerator:

    # initialize attributes
    moves = []
    #board = None
    enemy_players = []
    opponent_sliding_attack_map = 0

    friendly_king_square = 0
    opponent_attack_map = 0

    def __init__(self, board):
        self.in_check = False
        self.in_double_check = False
        self.pins_exist_in_position = False
        self.check_ray_bitmask = 0
        self.pin_ray_bitmask = 0

        self.board = board
        self.enemy_players = board.current_enemy_players
        self.friendly_king_square = self.board.king_square.get(board.next_to_move())

        self.north_has_king_castle_right = True
        self.north_has_queen_castle_right = True
        self.south_has_king_castle_right = True
        self.south_has_queen_castle_right = True
        self.west_has_king_castle_right = True
        self.west_has_queen_castle_right = True
        self.east_has_king_castle_right = True
        self.east_has_queen_castle_right = True

        self.enemy_queens = self.board.queens[:self.board.next_to_move] + self.board.queens[self.board.next_to_move + 1:]
        self.enemy_rooks = self.board.rooks[:self.board.next_to_move] + self.board.rooks[self.board.next_to_move + 1:]
        self.enemy_bishops = self.board.bishops[:self.board.next_to_move] + self.board.bishops[self.board.next_to_move + 1:]
        self.enemy_knights = self.board.knights[:self.board.next_to_move] + self.board.knights[self.board.next_to_move + 1:]
        self.enemy_pawns = self.board.pawns[:self.board.next_to_move] + self.board.pawns[self.board.next_to_move + 1:]
        self.enemy_kings = self.board.kings[:self.board.next_to_move] + self.board.kings[self.board.next_to_move + 1:]

        self.generate_moves()

    # generates all legal moves for a given position
    def generate_moves(self):

        self.calculate_attack_data()
        self.generate_king_moves()

        # self.moves.append(Move(None, 75, 89))
        # return self.moves

    def generate_sliding_attack_map(self):
        self.opponent_sliding_attack_map = 0
        for rook in self.enemy_rooks:
            self.update_sliding_attack_piece(self.enemy_rooks[rook], 0, 4)  # direction offsets
        for bitch in self.enemy_queens:
            self.update_sliding_attack_piece(self.enemy_queens[bitch], 0, 8)
        for bhop in self.enemy_bishops:
            self.update_sliding_attack_piece(self.enemy_bishops[bhop], 4, 8)

    def update_sliding_attack_piece(self, start_square, start_dir_index, end_dir_index):
        for direction_index in range(start_dir_index, end_dir_index, 1):
            current_offset = direction_offsets[direction_index]
            for step in range(num_squares_to_edge[start_square][direction_index]):
                target_square = start_square + current_offset * (step + 1)
                target_square_piece = self.board.square[target_square]
                self.opponent_sliding_attack_map |= 1 << target_square
                if target_square != self.friendly_king_square:
                    if target_square_piece != piece.Piece.none:
                        break

    def calculate_attack_data(self):
        self.generate_sliding_attack_map()

        # check for checks and pins around own king
        # check sliding pieces
        start_dir_index = 0
        end_dir_index = 0

        if not self.enemy_queens:  # if list empty
            start_dir_index = 0 if not self.enemy_rooks else 4
            end_dir_index = 8 if not self.enemy_bishops else 4

        for dir in range(start_dir_index, end_dir_index, 1):
            is_diagonal = dir > 3

            n = num_squares_to_edge[self.friendly_king_square][dir]
            direction_offset = direction_offsets[dir]
            friendly_piece_along_way = False
            ray_mask = 0

            for i in range(n):
                square_index = self.friendly_king_square + direction_offset * (i + 1)
                ray_mask |= 1 << square_index
                current_piece = self.board.square[square_index]

                # square contains a piece
                if current_piece is not piece.Piece.none:
                    if piece.Piece.is_player(current_piece, self.board.next_to_move):

                        # first friendly piece for this direction, so might be pinned
                        if not friendly_piece_along_way:
                            friendly_piece_along_way = True

                        # second piece in that direction, so no pin is possible
                        else:
                            break

                    # square contains enemy
                    else:
                        piece_type = piece.Piece.piece_type(current_piece)

                        # check if piece is able to move:
                        if (is_diagonal and piece.Piece.is_bishop_or_queen(piece_type)) or \
                            (not is_diagonal and piece.Piece.is_rook_or_queen(piece_type)):

                            # if friendly piece blocks a check its a pin
                            if friendly_piece_along_way:
                                self.pins_exist_in_position = True
                                self.pin_ray_bitmask |= ray_mask

                            # no friendly piece blocking so its check
                            else:
                                self.check_ray_bitmask |= ray_mask
                                self.in_double_check = self.in_check  # if already check now double
                                self.in_check = True
                            break

                        else:
                            # current enemy piece not able to move into this direction so break
                            break

            # no need to search for pins in double check since only king moves allowed anyways
            if self.in_double_check:
                break

        # check for knight attacks
        opponent_knight_attacks = 0
        is_knight_check = False

        for knight in self.enemy_knights:  # knight is the int square number
            opponent_knight_attacks |= knight_attack_bitboards.get(knight)

            if not is_knight_check and bitboard_contains_square(opponent_knight_attacks, self.friendly_king_square):
                is_knight_check = True
                self.in_double_check = self.in_check
                self.in_check = True
                self.check_ray_bitmask |= 1 << knight

        # check for pawn attacks
        opponent_pawn_attack_map = 0
        is_pawn_check = False

        for pawn in self.enemy_pawns:
            pawn_attacks = 0
            pawn_square = self.enemy_pawns[pawn]
            for enemy in self.enemy_players:
                pawn_attacks |= pawn_attack_bitboards[pawn][enemy]  # TODO: test if this works for all enemies, not sure whether summing them up like this works properly
                opponent_pawn_attack_map |= pawn_attacks

            if not is_pawn_check and bitboard_contains_square(pawn_attacks, self.friendly_king_square):
                is_pawn_check = True
                self.in_double_check = self.in_check
                self.in_check = True
                self.check_ray_bitmask |= 1 << pawn_square

        # check for kings
        opponent_king_attacks = 0
        for king in self.enemy_kings:
            opponent_king_attacks |= king_attack_bitboards[king]

        opponent_attack_map_no_pawns = self.opponent_sliding_attack_map | opponent_king_attacks | opponent_king_attacks  # TODO: check scopes, do I need them as attributes like sliding or not? make all the same!
        self.opponent_attack_map = opponent_attack_map_no_pawns | opponent_pawn_attack_map

    def square_is_attacked(self, square):
        return bitboard_contains_square(self.opponent_attack_map, square)

    def square_is_in_check_ray(self, square):
        return self.in_check and ((self.check_ray_bitmask >> square) & 1) != 0

    def generate_king_moves(self):
        for i in range(len(king_moves[self.friendly_king_square])):
            target_square = king_moves[self.friendly_king_square][i]
            piece_on_target_square = self.board.square[target_square]

            # skip if own piece is on square
            if piece.Piece.is_player(piece_on_target_square, self.board.next_to_move):
                continue

            is_capture = False
            for enemy in self.enemy_players:
                is_capture |= piece.Piece.is_player(piece_on_target_square, enemy)  # TODO: test whether this works as intended

            if not is_capture:
                # King can't move into square controlled by enemy unless it captures
                if self.square_is_in_check_ray(target_square):
                    continue

            # King can move to this square
            if not self.square_is_attacked(target_square):
                self.moves.append(Move(self.friendly_king_square, target_square))

                # Castling
                if not self.in_check and not is_capture:

                    # Need to differentiate between four players
                    if self.board.next_to_move == NORTH_INDEX:
                        if target_square == 5 and self.north_has_king_castle_right:
                            castle_kingside_square = target_square - 1  # King moves 2 positions
                            if self.board.square[castle_kingside_square] == piece.Piece.none:
                                if not self.square_is_attacked(castle_kingside_square):
                                    self.moves.append(Move(self.friendly_king_square, castle_kingside_square, Move.Flag.CASTLING))

                        # TODO: implement the other 7 possible castle directions
                        if target_square == 8 and self.north_has_queen_castle_right:
                            castle_queenside_square = target_square + 1
                            if self.board.square[castle_queenside_square] == piece.Piece.none:
                                if not self.square_is_attacked(castle_queenside_square):
                                    self.moves.append(
                                        Move(self.friendly_king_square, castle_queenside_square, Move.Flag.CASTLING))

                    if self.board.next_to_move == SOUTH_INDEX:
                        pass
