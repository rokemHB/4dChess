from chess.pieces.piece import Piece


class Pawn(Piece):

    def __init__(self, squareNr, player):
        super().__init__(squareNr, player)

    def get_draw_info(self):
        return self.player + "p"





# legaler move hängt vom player ab: north player darf nur runter, west player nur nach rechts etc.