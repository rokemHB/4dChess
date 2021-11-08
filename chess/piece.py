class Piece:

    # bit representations
    none = 0
    king = 1
    pawn = 2
    knight = 3
    bishop = 5  # check is_sliding_piece() why it's 5 not 4
    rook = 6
    queen = 7

    north = 8
    south = 16
    west = 32
    east = 64

    type_mask  = 0b0000111
    north_mask = 0b0001000
    south_mask = 0b0010000
    west_mask  = 0b0100000
    east_mask  = 0b1000000
    player_mask = north_mask | south_mask | west_mask | east_mask

    def is_player(self, piece, player):  # color in 2 player chess
        return (piece & self.player_mask) == player

    def player(self, piece):
        return piece & self.player_mask

    def piece_type(self, piece):
        return piece & self.type_mask

    def is_sliding_piece(self, piece):
        return (piece & 0b100) != 0

    # for checking orthogonal / diagonal rays
    def is_rook_or_queen(self, piece):
        return (piece & 0b110) == 0b110

    def is_bishop_or_queen(self, piece):
        return (piece & 0b101) == 0b101



