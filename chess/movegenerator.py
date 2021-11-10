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

        # check for checks and pins
        start_dir_index = 0
        end_dir_index = 0

        if not self.enemy_queens:  # if list empty
            start_dir_index = 0 if not self.enemy_rooks else 4
            end_dir_index = 8 if not self.enemy_bishops else 4

        for dir in range(start_dir_index, end_dir_index, 1):
            pass
            # stuff
