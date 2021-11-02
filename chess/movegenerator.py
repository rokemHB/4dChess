import numpy as np

# much logic adapted to 4 player chess from https://github.com/SebLague/Chess-AI/

# bitboards paper: https://www2.teu.ac.jp/gamelab/RESEARCH/ICGAJournal2007.pdf
# TODO: need 196 bit integer for bitboards, is that possible? --> Seems so, dont know about performance though
#       could take multiple 64 bit integers, but 196 / 64 > 3 so 4 ints needed ....
# rotated bitmaps: https://sci-hub.st/10.3233/ICG-1999-22403


# 4 orthogonal and 4 diagonal directions (N, S, W, E, NW, SE, NE, SW)
from chess import board
from chess.constants import DEAD_SQUARES, SQUARE_SIZE

direction_offsets = [-14, 14, -1, 1, -15, 15, -13, 13]
knight_offsets = [-16, -29, -27, -12, 16, 29, 27, 12]

# For every square, stores number of squares to the edge for all 8 direction for given position
# 196 x 8 matrix for 8 direction_offsets
numSquaresToEdge = [[0 for x in range(8)] for y in range(196)]

# TODO: the 0s are bad in here, not sure how to make array 196 long and dynamically add to each of the 196 lists?!
#   0 still kinda okay since 0 is dead square in 4p chess
knight_moves = [[0 for x in range(8)] for y in range(196)]

knight_attack_bitboards = dict()  # TODO: if this works make the others to dicts as well?


def precalculate_data():

    for square_nr in range(0, 196):

        if is_inside_board(square_nr):
            # orthogonal directions:
            # fill steps to edge for each direction and each square_nr
            y = square_nr // 14
            x = square_nr - y * 14  # probably faster than square_nr % 14

            # exclude dead squares in the corners of 4 player chess board
            if 2 < x < 11:
                north = y
                south = 13 - y
                if 2 < y < 11:
                    west = x
                    east = 13 - x
                else:  # y < 3 or y > 11
                    west = x - 3
                    east = 10 - x
            else:  # x < 2 or x > 11
                north = y - 3
                south = 10 - y
                west = x
                east = 13 - x

            numSquaresToEdge[square_nr][0] = north
            numSquaresToEdge[square_nr][1] = south
            numSquaresToEdge[square_nr][2] = west
            numSquaresToEdge[square_nr][3] = east

            # diagonal directions:
            # counts offset index
            j = 4
            for offset in direction_offsets[4:8]:
                i = 0
                while is_inside_board(i * offset + square_nr):

                    # make sure we can not jump from left to right side by comparing x coordinates. This
                    #   can otherwise happen if the wrap around square is legal
                    if abs(board.get_coordinates_from_square_nr(i * offset + square_nr)[0] -
                           board.get_coordinates_from_square_nr((i + 1) * offset + square_nr)[0]) > (2 * SQUARE_SIZE):
                        i += 1  # still add for this round but stop then
                        break
                    else:
                        i += 1
                numSquaresToEdge[square_nr][j] = i - 1
                j += 1
        else:  # dont fill dead squares
            continue

        ### ----------------------- ###
        # knight moves with bitboards #
        ### ----------------------- ###

        knight_bitboard = 0

        k = 0

        for knight_jump_offset in knight_offsets:
            knight_jump_square = square_nr + knight_jump_offset
            if is_inside_board(knight_jump_square):

                # get respective x and y coordinates of target square
                knight_square_y = knight_jump_square // 14
                knight_square_x = knight_jump_square - knight_square_y * 14

                # make sure no wrap around sides of board
                max_move_distance = max(abs(x - knight_square_x), abs(y - knight_square_y))
                if max_move_distance == 2:
                    knight_moves[square_nr][k] = knight_jump_square

                    # set 1 for square position in knight bitboard
                    knight_bitboard |= 1 << knight_jump_square

        knight_attack_bitboards[square_nr] = knight_bitboard  # TODO: try this as dict








def is_inside_board(square_nr):
    """
    checks whether a given square number is within board limits
    """
    return 2 < square_nr < 193 and square_nr not in DEAD_SQUARES


precalculate_data()
print(numSquaresToEdge[73])
# [5, 8, 5, 8, 2, 5, 5, 6] --> letzte 6 ist falsch!

print(bin(knight_attack_bitboards.get(73)))
