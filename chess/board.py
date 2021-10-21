import pygame

from chess.constants import *
from chess.pieces.pawn import Pawn


class Board:
    IMAGES = {}

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
        self.board[17] = Pawn(3, 'n')
        self.board[18] = Pawn(4, 'n')
        self.board[19] = Pawn(5, 'n')
        self.board[20] = Pawn(6, 'n')
        self.board[21] = Pawn(7, 'n')
        self.board[22] = Pawn(8, 'n')
        self.board[23] = Pawn(9, 'n')
        self.board[24] = Pawn(10, 'n')
        self.load_images()
        self.draw_pieces(win)

    def load_images(self):
        pieces = ['sp', 'sR', 'sN', 'sB', 'sK', 'sQ', 'np', 'nR', 'nN', 'nB', 'nK', 'nQ']
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
