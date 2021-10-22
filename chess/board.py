import pygame

from chess.constants import *
from chess.pieces.bishop import Bishop
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook


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

    def __init__(self):
        self.board = [None] * 196
        self.selected_piece = None  # TODO: Needed?

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

    def new_game(self, win):
        """
        Initiates new game
        Sets pieces into start position
        Loads images
        """
        for piece in self.startPositions:
            self.board[piece.get_square()] = piece

        self.load_images()  # make sure this only gets called once!

    def load_images(self):
        """
        Loads images to memory
        Needs absolute path on windows for some reason, on linux relative path is fine
        """
        pieces = ['sP', 'sR', 'sN', 'sB', 'sK', 'sQ', 'nP', 'nR', 'nN', 'nB', 'nK', 'nQ',
                  'wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'eP', 'eR', 'eN', 'eB', 'eK', 'eQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(
                pygame.image.load("C:/Users/kemmeri/Git/4dChess/chess/images/" + piece + ".png"),
                (SQUARE_SIZE, SQUARE_SIZE))

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

    def coordinates_to_square(self, pos):
        """
        Returns the square number for given x and y coordinates
        """
        x_square = pos[0] // SQUARE_SIZE  # integer division
        y_square = pos[1] // SQUARE_SIZE
        return int(x_square + 14 * y_square)

    def get_square_coordinates(self, pos):
        """
        Returns the top left square corner coordinates of a given coordinate
        """
        corner_pos = []
        corner_pos[0] = (pos[0] // SQUARE_SIZE) * SQUARE_SIZE
        corner_pos[1] = (pos[1] // SQUARE_SIZE) * SQUARE_SIZE
        return corner_pos

    def click(self, pos):
        """
        Event for pressing down a mouse button
        Returns the piece object on the respective square
        """
        clicked_square = self.board[self.coordinates_to_square(pos)]  # gets the piece object
        return clicked_square

    def drag(self, pos, win):
        """
        Event for moving the mouse, only relevant after a mouse button has been clicked
        Draws the piece centered on the cursor
        """
        filename = self.selected_piece.get_draw_info()
        win.blit(self.IMAGES[filename], (pos[0] - SQUARE_SIZE / 2, pos[1] - SQUARE_SIZE / 2))

    def make_move(self, new_pos):
        """
        Executes a move command, setting new positions and update drawings on board
        Does not check whether move is legal
        """
        if self.selected_piece is not None:
            old_square = self.selected_piece.get_square()
            new_square = self.coordinates_to_square(new_pos)

            if old_square == new_square:
                return
            else:
                self.board[old_square] = None
                self.selected_piece.set_square(new_square)
                self.board[new_square] = self.selected_piece
                self.selected_piece = None
        else:
            print("No piece is selected")

    def get_square_color(self, pos):
        """
        Calculates color of a square given coordinates
        0 = White, 1 = Black
        """
        square_nr = self.coordinates_to_square(pos)
        return ((square_nr % 14) + (square_nr // 14)) % 2
