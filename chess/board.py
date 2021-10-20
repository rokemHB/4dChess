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

    def new_game(self, win):
        self.board[3] = Pawn(3)
        self.board[4] = Pawn(4)
        self.board[5] = Pawn(5)
        self.board[6] = Pawn(6)
        self.board[7] = Pawn(7)
        self.board[8] = Pawn(8)
        self.board[9] = Pawn(9)
        self.board[10] = Pawn(10)
        self.load_images()
        self.draw_pieces(win)

    def load_images(self):
        pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
        for piece in pieces:
            self.IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),
                                                        (SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, win):
        i = 0
        for row in range(ROWS):
            for col in range(COLS):
                print(i)
                print(self.board[i] is not None)
                if self.board[i] is not None:
                    win.blit(self.IMAGES['bp'], (col * SQUARE_SIZE, row * SQUARE_SIZE))

                i += 1
