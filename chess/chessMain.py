import pygame

from chess.board import Board
from chess.constants import *  # TODO: might wanna specify if more constants get added

# -5 to kill little bar due to rounding errors, take less when scaling down window size
WIN = pygame.display.set_mode((WIDTH-5, HEIGHT-5))
pygame.display.set_caption('testChess')

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 10)

clock = pygame.time.Clock()


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("green"))
    return fps_text


def main():
    run = True

    board = Board()

    board.new_game(WIN)

    # whether piece should be drawn on curser position
    piece_drag = False

    # keep track of whose turn it is
    players = ['n', 'e', 's', 'w']
    currentPlayer = 0

    while run:
        clock.tick(FPS)

        board.draw_squares(WIN)
        #board.draw_numbers(WIN, font)
        board.draw_pieces(WIN)

        WIN.blit(update_fps(), (WIDTH - 20, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if board.click(pygame.mouse.get_pos(), players[currentPlayer], WIN):
                    piece_drag = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if board.make_move(pygame.mouse.get_pos(), WIN):
                    currentPlayer = (currentPlayer + 1) % 4
                piece_drag = False

            elif event.type == pygame.MOUSEMOTION:
                if piece_drag:
                    board.drag(pygame.mouse.get_pos(), WIN)
                elif board.selected_piece is not None:
                    board.draw_legal_moves(WIN)

            pygame.display.update()

    pygame.quit()


main()
