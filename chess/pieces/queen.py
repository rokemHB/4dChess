from chess.pieces.piece import Piece


class Queen(Piece):

    def __init__(self, square_nr, player):
        super().__init__(square_nr, player)

    def get_draw_info(self):
        return self.player + "Q"

