from chess.pieces.piece import Piece


class Bishop(Piece):

    def __init__(self, square_nr, player):
        super().__init__(square_nr, player)

    def get_draw_info(self):
        return self.player + "B"

