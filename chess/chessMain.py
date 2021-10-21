import pygame

from chess.board import Board
from chess.constants import *  # might wanna specify if more constants get added

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('testChess')

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 9)


def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()

    board.new_game(WIN)

    piece_drag = False
    temp_piece = None

    while run:
        clock.tick(FPS)

        board.draw_squares(WIN)
        board.draw_numbers(WIN, font)
        board.draw_pieces(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                temp_piece = board.click2(pygame.mouse.get_pos())
                piece_drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                piece_drag = False

            elif event.type == pygame.MOUSEMOTION:
                if piece_drag:
                    # mouse_x, mouse_y = event.pos
                    board.drag(pygame.mouse.get_pos(), temp_piece, WIN)

            pygame.display.update()

    pygame.quit()


main()
