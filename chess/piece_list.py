class Piece_list:

    def __init__(self):
        self.occupied_squares = []
        self.map = [None] * 196  # saves the index of occupied_squares
        self.num_pieces = 0

    # python index handling - allows piece_list[1] instead of piece_list.occupied_squares[1] to get item
    def __getitem__(self, piece):
        return self.occupied_squares[piece]

    def add_piece_at_square(self, square_nr):
        self.occupied_squares[self.num_pieces] = square_nr
        self.map[square_nr] = self.num_pieces
        self.num_pieces += 1

    def remove_piece_at_square(self, square_nr):
        piece_index = self.map[square_nr]
        self.occupied_squares[piece_index] = self.occupied_squares[piece_index - 1]  # move last element to deleted el
        self.map[self.occupied_squares[piece_index]] = piece_index  # point map to new moved location
        self.num_pieces -= 1

    def move_piece(self, start_square, target_square):
        piece_index = self.map[start_square]
        self.occupied_squares[piece_index] = target_square
        self.map[target_square] = piece_index