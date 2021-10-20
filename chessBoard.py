import pygame

WIDTH, HEIGHT = 1000, 1000

ROWS, COLS = 14, 14
SQUARE_SIZE = WIDTH // COLS

WHITE = (200, 200, 200)
BLACK = (40, 40, 40)

FPS = 60

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

            pygame.display.update()

    pygame.quit()


# set of dead corner squares
DEAD_SQUARES = {0, 1, 2, 11, 12, 13, 14, 15, 16, 25, 26, 27, 28, 29, 30, 39, 40, 41,
                154, 155, 156, 165, 166, 167, 168, 169, 170, 179, 180, 181, 182, 183, 184, 193, 194, 195}


# outsource to own file
class Board:
    def __init__(self):
        self.board = []
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


main()
