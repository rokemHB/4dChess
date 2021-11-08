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

        self.generate_moves()

    # generates all legal moves for a given position
    def generate_moves(self):

        self.calculate_attack_data()

        # self.moves.append(Move(None, 75, 89))
        # return self.moves

    def generate_sliding_attack_map(self):
        self.opponent_sliding_attack_map = 0

        enemy_rooks = []
        for enemy in self.enemy_players:
            enemy_rooks.append(self.board.rooks[enemy])
        for rook in enemy_rooks:
            self.update_sliding_attack_piece(enemy_rooks[rook], 0, 4)  # direction offsets

        enemy_queens = []
        for enemy in self.enemy_players:
            enemy_queens.append(self.board.queens[enemy])
        for bitch in enemy_queens:
            self.update_sliding_attack_piece(enemy_queens[bitch], 0, 8)

        enemy_bishops = []
        for enemy in self.enemy_players:
            enemy_bishops.append(self.board.bishops[enemy])
        for bhop in enemy_bishops:
            self.update_sliding_attack_piece(enemy_bishops[bhop], 4, 8)

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

        enemy_queens = []
        for enemy in self.enemy_players:
            enemy_queens.append(self.board.queens[enemy])  # TODO: this is retarded, need to make access for all but own pieces easier! -> auch Bitmaske oder sowas? ohne loopen...
        if not enemy_queens:  # if list empty
            enemy_rooks = []
            enemy_bishops = []
            for enemy in self.enemy_players:
                enemy_rooks.append(self.board.rooks[enemy])
            start_dir_index = 0 if not enemy_rooks else start_dir_index = 4
            end_dir_index = 8 if not enemy_bishops else end_dir_index = 4

        for dir in range(start_dir_index, end_dir_index, 1):
            pass
            # stuff
