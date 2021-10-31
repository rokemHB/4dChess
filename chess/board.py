import pygame

from chess.constants import *
from chess.movegenerator import legal_moves, is_inside_board, check_checker
from chess.pieces.bishop import Bishop
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook

# TODO: remove if not needed
""" 
def get_square_color(pos):

    Calculates color of a square given coordinates
    0 = White, 1 = Black

    square_nr = coordinates_to_square(pos)
    return ((square_nr % 14) + (square_nr // 14)) % 2
    
    
def square_to_coordinates(pos):

    Returns the top left square corner coordinates of a given coordinate

    corner_pos = []
    corner_pos.append((pos[0] // SQUARE_SIZE) * SQUARE_SIZE)
    corner_pos.append((pos[1] // SQUARE_SIZE) * SQUARE_SIZE)
    return corner_pos
"""


class Board:
    # stores the piece pngs
    IMAGES = {}

    # standard start position - north / south / west / east
    startPositions = [
        Pawn(17, 'n'), Pawn(18, 'n'), Pawn(19, 'n'), Pawn(20, 'n'),
        Pawn(21, 'n'), Pawn(22, 'n'), Pawn(23, 'n'), Pawn(24, 'n'),
        Rook(3, 'n'), Rook(10, 'n'), Knight(4, 'n'), Knight(9, 'n'),
        Bishop(5, 'n'), Bishop(8, 'n'), King(6, 'n'), Queen(7, 'n'),

        Pawn(171, 's'), Pawn(172, 's'), Pawn(173, 's'), Pawn(174, 's'),
        Pawn(175, 's'), Pawn(176, 's'), Pawn(177, 's'), Pawn(178, 's'),
        Rook(185, 's'), Rook(192, 's'), Knight(186, 's'), Knight(191, 's'),
        Bishop(187, 's'), Bishop(190, 's'), King(189, 's'), Queen(188, 's'),

        Pawn(43, 'w'), Pawn(57, 'w'), Pawn(71, 'w'), Pawn(85, 'w'),
        Pawn(99, 'w'), Pawn(113, 'w'), Pawn(127, 'w'), Pawn(141, 'w'),
        Rook(42, 'w'), Rook(140, 'w'), Knight(56, 'w'), Knight(126, 'w'),
        Bishop(70, 'w'), Bishop(112, 'w'), King(84, 'w'), Queen(98, 'w'),

        Pawn(54, 'e'), Pawn(68, 'e'), Pawn(82, 'e'), Pawn(96, 'e'),
        Pawn(110, 'e'), Pawn(124, 'e'), Pawn(138, 'e'), Pawn(152, 'e'),
        Rook(55, 'e'), Rook(153, 'e'), Knight(69, 'e'), Knight(139, 'e'),
        Bishop(83, 'e'), Bishop(125, 'e'), King(111, 'e'), Queen(97, 'e')
    ]

    move_list = []

    def __init__(self):
        self.board = [None] * 196
        self.selected_piece = None
        # safe king positions (square_nr) to check for check - defaults are start positions
        self.king_pos = {'n': 6, 'e': 111, 's': 189, 'w': 84}
        # TIL: when attribute is not in constructor, making deepcopy of class will point to same memory of attribute,
        #      so that changing the copy will still change the original. Calling it in constructor prevents it.

    def draw_squares(self, win):
        """
        Draws the squares of the board
        """
        win.fill(BLACK)
        i = 0
        for row in range(ROWS):

            # chess board
            for col in range(row % 2, ROWS, 2):
                # all regular squares of the game
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # dead corners
            for col in range(COLS):
                if i in DEAD_SQUARES:
                    pygame.draw.rect(win, (135, 206, 235), (row * SQUARE_SIZE, col * SQUARE_SIZE,
                                                            SQUARE_SIZE, SQUARE_SIZE))
                i += 1

    def draw_numbers(self, win, thisfont):
        """
        Draws numbers to bottom left corner of squares
        Mainly for testing purposes
        Might be replaced with classical Letter x Number system
        """
        i = 0
        for row in range(ROWS):
            for col in range(COLS):
                number = thisfont.render(str(i), True, (255, 0, 0))
                win.blit(number, (col * SQUARE_SIZE + SQUARE_SIZE / 15, row * SQUARE_SIZE + SQUARE_SIZE / 1.13))
                i += 1

    def get_coordinates_from_square_nr(self, square_nr):
        """
        calculates top left corner coordinates for a given square number
        """
        res = []
        res.append((square_nr % 14) * SQUARE_SIZE)
        res.append((square_nr // 14) * SQUARE_SIZE)
        return res

    def coordinates_to_square(self, pos):
        """
        Returns the square number for given x and y coordinates
        """
        x_square = pos[0] // SQUARE_SIZE  # integer division
        y_square = pos[1] // SQUARE_SIZE
        return int(x_square + 14 * y_square)

    def new_game(self, win):
        """
        Initiates new game
        Sets pieces into start position
        Loads images
        """
        for piece in self.startPositions:
            self.set_piece(piece.get_square(), piece)

        self.load_images()  # make sure this only gets called once!

    def set_piece(self, square_nr, piece):
        self.board[square_nr] = piece

    def get_piece(self, square_nr):
        if is_inside_board(square_nr):
            return self.board[square_nr]
        else:
            return None

    def load_images(self, path="images/"):
        """  C:/Users/kemmeri/Git/4dChess/chess/
        Loads images to memory
        Needs absolute path on windows for some reason, on linux relative path is fine
        path given as parameter so test class in different package can also use it ...
        """
        pieces = ['sP', 'sR', 'sN', 'sB', 'sK', 'sQ', 'nP', 'nR', 'nN', 'nB', 'nK', 'nQ',
                  'wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'eP', 'eR', 'eN', 'eB', 'eK', 'eQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(
                pygame.image.load(path + piece + ".png"),
                (int(SQUARE_SIZE), int(SQUARE_SIZE)))  # C:/Users/kemmeri/Git/4dChess/chess/

        symbols = ['green_dot', 'grey_dot']
        for symbol in symbols:
            self.IMAGES[symbol] = pygame.transform.scale(
                pygame.image.load(path + symbol + ".png"),
                (int(SQUARE_SIZE / 2), int(SQUARE_SIZE / 2)))

    def draw_pieces(self, win):
        """
        Draws pieces for all squares on the board
        """
        i = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[i] is not None:
                    filename = self.board[i].get_draw_info()
                    win.blit(self.IMAGES[filename], (col * SQUARE_SIZE, row * SQUARE_SIZE))

                i += 1

    def click(self, pos, player, win):
        """
        Event for pressing down a mouse button
        Returns the piece object on the respective square
        """
        if check_checker(player, self, False):
            print("TESTCHECKERMOTHERFUCKER!!!!!!!!!!!") # How to filter moves now for anti check only?
            # idee: noch ne flag, in_check = True, diese in legal_moves() einbringen. Wenn True, in jeder
            #       iteration prüfen, ob dann noch in check. Performance will be shit ...
        coor = self.coordinates_to_square(pos)
        if self.board[coor] is None:
            if coor not in self.move_list:
                self.move_list = []
            return False
        elif self.board[coor].get_player() == player:
            self.selected_piece = self.board[coor]
            self.move_list = legal_moves(self.selected_piece, self)
            self.draw_legal_moves(win)
            return True
        elif self.board[coor].get_player() != player:
            self.move_list = legal_moves(self.selected_piece, self)
        else:
            self.move_list = []
            return False

    def drag(self, pos, win):
        # TODO: SAFE LEGAL MOVES; DONT MAKE THE CALCULATION FOR EVERY TICK!
        """
        Event for moving the mouse, only relevant after a mouse button has been clicked
        Draws the piece centered on the cursor
        """
        self.draw_legal_moves(win)
        filename = self.selected_piece.get_draw_info()
        win.blit(self.IMAGES[filename], (pos[0] - SQUARE_SIZE / 2, pos[1] - SQUARE_SIZE / 2))

    def make_move(self, new_pos, win):
        """
        Executes a move command, setting new positions and update drawings on board
        Does not check whether move is legal
        """
        # TODO: Make Pawn to Queen when walked to opposite side of the board
        if self.selected_piece is not None:

            self.draw_legal_moves(win)

            old_square = self.selected_piece.get_square()
            new_square = self.coordinates_to_square(new_pos)

            if old_square == new_square:
                return False
            else:
                # check if move is legal
                if new_square in self.move_list:

                    self.board[old_square] = None
                    self.selected_piece.set_square(new_square)

                    if isinstance(self.selected_piece, Pawn):  # make queen when pawn at opposite end of board
                        if self.selected_piece.get_player() == 'n' and new_square > 184:
                            self.selected_piece = Queen(new_square, 'n')
                        if self.selected_piece.get_player() == 's' and new_square < 11:
                            self.selected_piece = Queen(new_square, 's')
                        if self.selected_piece.get_player() == 'w' and new_square in [55, 69, 83, 97, 111, 125, 139,
                                                                                      153]:
                            self.selected_piece = Queen(new_square, 'w')
                        if self.selected_piece.get_player() == 'e' and new_square in [42, 56, 70, 84, 98, 112, 126,
                                                                                      140]:
                            self.selected_piece = Queen(new_square, 'e')

                    # TODO: need to make sure that own movement does not put me into check
                    elif isinstance(self.selected_piece, King):
                        self.king_pos[self.selected_piece.get_player()] = self.coordinates_to_square(new_pos)

                    self.board[new_square] = self.selected_piece
                    self.selected_piece = None

                    self.draw_squares(win)
                    self.draw_pieces(win)

                    return True
                else:
                    return False
        else:
            print("No piece is selected")

    def draw_legal_moves(self, win):
        """
        draws circles to the board for all legal moves
        """

        # hier muss nun geguckt werden ob player im schach steht, und falls ja,
        # dürfen nur moves generiert werden, die dies ändern.

        if not self.move_list:  # empty list is False in python (all sequences)
            return
        else:
            for mv in self.move_list:
                coordinates = self.get_coordinates_from_square_nr(mv)
                win.blit(self.IMAGES['green_dot'],
                         (int(coordinates[0] + SQUARE_SIZE / 4),  # TODO: replace green by grey dot when not ur turn
                          int(coordinates[1] + SQUARE_SIZE / 4)))
