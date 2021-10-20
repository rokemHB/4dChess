import pygame

from chess.board import Board
from chess.constants import *  # might wanna specify if more constants get added


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('testChess')

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 15)




def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()


    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            board.draw_squares(WIN)
            board.draw_numbers(WIN, font)
            board.new_game(WIN)
            board.draw_pieces(WIN)

            pygame.display.update()

    pygame.quit()


main()
