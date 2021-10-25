import pygame

from chess.board import Board
from chess.constants import *  # TODO: might wanna specify if more constants get added

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('testChess')

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 9)

clock = pygame.time.Clock()


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def main():
    run = True

    board = Board()

    board.new_game(WIN)

    piece_drag = False
    temp_piece = None

    while run:
        clock.tick(FPS)

        board.draw_squares(WIN)
        # board.draw_numbers(WIN, font)
        board.draw_pieces(WIN)

        WIN.blit(update_fps(), (10, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.click(pygame.mouse.get_pos(), WIN)
                if board.selected_piece is not None:
                    piece_drag = True

                    ### selected piece lassen wenn nichts gemoved wird und dann mit movement generator die legalen züge auf dem Feld einblenden

            elif event.type == pygame.MOUSEBUTTONUP:
                board.make_move(pygame.mouse.get_pos(), WIN)
                piece_drag = False

            elif event.type == pygame.MOUSEMOTION:
                if piece_drag:
                    board.drag(pygame.mouse.get_pos(), WIN)
                elif board.selected_piece is not None:
                    board.draw_legal_moves(WIN)

            pygame.display.update()

    pygame.quit()


main()
