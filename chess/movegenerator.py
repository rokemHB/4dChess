from chess.move import Move


class MoveGenerator:

    # initialize attributes
    moves = []
    board = None
    enemy_players = []
    opponent_sliding_attack_map = 0

    def __init__(self, board):
        self.board = board
        self.enemy_players = board.current_enemy_players

    # generates all legal moves for a given position
    def generate_moves(self):
        # Flags
        in_check = False
        in_double_check = False
        pins_exist_in_position = False
        check_ray_bitmask = 0
        pin_ray_bitmask = 0

        # color to move ....
        pass

        # self.moves.append(Move(None, 75, 89))
        # return self.moves

    def generate_sliding_attack_map(self):
        self.opponent_sliding_attack_map = 0

        enemy_rooks = []
        for epl in self.enemy_players:
            enemy_rooks.append(self.board.rooks[epl])
        for piece in enemy_rooks:
            self.update_sliding_attack_piece(enemy_rooks[piece], 0, 4)  # direction offsets

        enemy_queens = []
        for epl in self.enemy_players:
            enemy_queens.append(self.board.queens[epl])
        for piece in enemy_queens:
            self.update_sliding_attack_piece(enemy_queens[piece], 0, 8)

        enemy_bishops = []
        for epl in self.enemy_players:
            enemy_bishops.append(self.board.bishops[epl])
        for piece in enemy_bishops:
            self.update_sliding_attack_piece(enemy_bishops[piece], 4, 8)

    def update_sliding_attack_piece(self, start_square, start_dir_index, end_dir_index):
        pass
