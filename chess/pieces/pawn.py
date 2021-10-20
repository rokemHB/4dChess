class Pawn:
    def __init__(self, square):
        self.square = square

        # legaler move hängt vom player ab: north player darf nur runter, west player nur nach rechts etc.