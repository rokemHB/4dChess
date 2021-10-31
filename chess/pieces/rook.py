from chess.pieces.piece import Piece


class Rook(Piece):

    def __init__(self, square_nr, player):
        super().__init__(square_nr, player)
        has_moved = False  # needed for castling

    def get_draw_info(self):
        return self.player + "R"

