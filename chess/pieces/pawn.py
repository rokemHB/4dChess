from chess.pieces.piece import Piece


class Pawn(Piece):

    def __init__(self, square_nr, player):
        super().__init__(square_nr, player)

    def get_draw_info(self):
        return self.player + "P"





# legaler move hängt vom player ab: north player darf nur runter, west player nur nach rechts etc.