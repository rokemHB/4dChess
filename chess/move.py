from enum import Enum

class Move:

    # my take on multiple constructors in python ...
    # can initiate a move by giving it a move_value, start and target, or additional flag
    def __init__(self, move_value=None, start_square=None, target_square=None, flag=None):

        if move_value is not None:
            self.move_value = move_value
        elif flag is None:
            self.move_value = start_square | target_square << 8
        else:
            self.move_value = start_square | target_square << 8 | flag << 12

    # inner class enum for flagging all special moves
    class Flag(Enum):
        NONE = 0
        EN_PASSANT_CAPTURE = 1
        CASTLING = 2
        PROMOTE_TO_QUEEN = 3
        PROMOTE_TO_KNIGHT = 4
        PROMOTE_TO_ROOK = 5
        PROMOTE_TO_BISHOP = 6
        PAWN_TO_FORWARD = 7

    # 4 bits for flag (8 values)
    # 8 bit for start square (196 values -> 8 bits = 256)
    # 8 bit for target square
    start_square_mask = 0b00000000000011111111
    target_square_mask = 0b00001111111100000000
    flag_mask = 0b11110000000000000000

    # get start/target square
    # bool is_promotion
    def get_move_flag(self):
        return self.move_value >> 16

    # get value





