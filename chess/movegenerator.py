from chess import piece
from chess.move import Move
from chess.precalculations import num_squares_to_edge, direction_offsets


class MoveGenerator:

    # initialize attributes
    moves = []
    #board = None
    #enemy_players = []
    opponent_sliding_attack_map = 0

    friendly_king_square = 0

    def __init__(self, board):
        self.in_check = False
        self.in_double_check = False
        self.pins_exist_in_position = False
        self.check_ray_bitmask = 0
        self.pin_ray_bitmask = 0

        self.board = board
        self.enemy_players = board.current_enemy_players
        self.friendly_king_square = self.board.king_square.get(board.get_next_to_move())

        self.enemy_queens = self.board.queens[:self.board.next_to_move] + self.board.queens[self.board.next_to_move + 1:]
        self.enemy_rooks = self.board.rooks[:self.board.next_to_move] + self.board.rooks[self.board.next_to_move + 1:]
        self.enemy_bishops = self.board.bishops[:self.board.next_to_move] + self.board.bishops[self.board.next_to_move + 1:]
        self.enemy_knights = self.board.knights[:self.board.next_to_move] + self.board.knights[self.board.next_to_move + 1:]

        self.generate_moves()

    # generates all legal moves for a given position
    def generate_moves(self):

        self.calculate_attack_data()

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


