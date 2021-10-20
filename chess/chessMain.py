import pygame

from chess.board import Board
from chess.constants import *  # might wanna specify if more constants get added


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('testChess')

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 15)

IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"),
                                               (SQUARE_SIZE, SQUARE_SIZE))


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    loadImages()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            board.draw_squares(WIN)
            board.draw_numbers(WIN, font)

            pygame.display.update()

    pygame.quit()


main()
