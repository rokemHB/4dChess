from chess.move import Move


class MoveGenerator:
    moves = []
    board = None

    def __init__(self, board):
        self.board = board

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
        pass
