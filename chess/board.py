import pygame

from chess.constants import *
from chess.pieces.bishop import Bishop
from chess.pieces.king import King
from chess.pieces.knight import Knight
from chess.pieces.pawn import Pawn
from chess.pieces.queen import Queen
from chess.pieces.rook import Rook


class Board:
    IMAGES = {}

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
        self.selected_piece = None

    def draw_squares(self, win):
        win.fill(BLACK)
        i = 0
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                # all regular squares of the game
                pygame.draw.rect(win, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            for col in range(COLS):
                if i in DEAD_SQUARES:
                    pygame.draw.rect(win, (135, 206, 235), (row * SQUARE_SIZE, col * SQUARE_SIZE,
                                                            SQUARE_SIZE, SQUARE_SIZE))
                i += 1

    def draw_numbers(self, win, thisfont):
        i = 0
        for row in range(ROWS):
            for col in range(COLS):
                number = thisfont.render(str(i), True, (255, 0, 0))
                win.blit(number, (col * SQUARE_SIZE + SQUARE_SIZE / 8, row * SQUARE_SIZE + SQUARE_SIZE / 1.3))
                i += 1

    # replace this with FEN positions at some point
    def new_game(self, win):
        for piece in self.startPositions:
            self.board[piece.get_square()] = piece

        self.load_images()  # move so it really gets only called once!
        self.draw_pieces(win)

    def load_images(self):
        pieces = ['sP', 'sR', 'sN', 'sB', 'sK', 'sQ', 'nP', 'nR', 'nN', 'nB', 'nK', 'nQ',
                  'wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'eP', 'eR', 'eN', 'eB', 'eK', 'eQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),
                                                        (SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win):
        i = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[i] is not None:
                    filename = self.board[i].get_draw_info()
                    win.blit(self.IMAGES[filename], (col * SQUARE_SIZE, row * SQUARE_SIZE))

                i += 1
