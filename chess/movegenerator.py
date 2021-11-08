from chess import board
from chess.constants import DEAD_SQUARES, SQUARE_SIZE, NORTH_INDEX, SOUTH_INDEX, WEST_INDEX, EAST_INDEX

# some logic adapted to 4 player chess from https://github.com/SebLague/Chess-AI/

# bitboards paper: https://www2.teu.ac.jp/gamelab/RESEARCH/ICGAJournal2007.pdf
# TODO: need 196 bit integer for bitboards, is that possible? --> Seems so, dont know about performance though
#       could take multiple 64 bit integers, but 196 / 64 > 3 so 4 ints needed ....
# rotated bitmaps publication: https://sci-hub.st/10.3233/ICG-1999-22403

# 4 orthogonal and 4 diagonal directions (N, S, W, E, NW, SE, NE, SW)
from chess.move import Move

direction_offsets = [-14, 14, -1, 1, -15, 15, -13, 13]
knight_offsets = [-16, -29, -27, -12, 16, 29, 27, 12]

# For every square, stores number of squares to the edge for all 8 direction for given position
numSquaresToEdge = dict()

# TODO: the 0s are bad in here, not sure how to make array 196 long and dynamically add to each of the 196 lists?!
#   0 still kinda okay since 0 is dead square in 4p chess
# --> CAN THIS ALSO BE REPLACED BY A DICT?
knight_moves = [[0 for x in range(8)] for y in range(196)]
king_moves = [[0 for x in range(8)] for y in range(196)]

knight_attack_bitboards = dict()
king_attack_bitboards = dict()

direction_lookup = dict()

pawn_attack_bitboards = [[0 for x in range(4)] for y in range(196)]
pawn_attacks_north = dict()
pawn_attacks_south = dict()
pawn_attacks_west = dict()
pawn_attacks_east = dict()

rook_moves = dict()
bishop_moves = dict()
queen_moves = dict()


def precalculate_data():
    for square_nr in range(0, 196):

        if is_inside_board(square_nr):

            ## ------------------------------------------------- ##
            # fill steps to edge for all directions per square_nr #
            ## ------------------------------------------------- ##

            temp_result = []

            # orthogonal directions:
            y = square_nr // 14
            x = square_nr - y * 14  # probably faster than square_nr % 14

            # exclude dead 3x3 squares in the corners of 4 player chess board
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

            # append the four orthogonal directions
            temp_result.extend([north, south, west, east])

            # diagonal directions:
            # counts offset index
            for offset in direction_offsets[4:8]:
                i = 0
                while is_inside_board(i * offset + square_nr):

                    # make sure no wrap around sides of board
                    # TODO: replace this with something less shit
                    if abs(board.get_coordinates_from_square_nr(i * offset + square_nr)[0] -
                           board.get_coordinates_from_square_nr((i + 1) * offset + square_nr)[0]) > (2 * SQUARE_SIZE):
                        i += 1  # still add for this round but stop then
                        break
                    else:
                        i += 1
                temp_result.append(i - 1)
            numSquaresToEdge[square_nr] = temp_result

            ## ------------------------- ##
            # knight moves with bitboards #
            ## ------------------------- ##

            knight_bitboard = 0
            k = 0

            for ofs in knight_offsets:
                knight_jump_square = square_nr + ofs
                if is_inside_board(knight_jump_square):

                    # get respective x and y coordinates of target square
                    knight_square_y = knight_jump_square // 14
                    knight_square_x = knight_jump_square - knight_square_y * 14

                    # make sure no wrap around sides of board
                    max_move_distance = max(abs(x - knight_square_x), abs(y - knight_square_y))
                    if max_move_distance == 2:
                        knight_moves[square_nr][k] = knight_jump_square  # TODO: how to deal with empty entries here? -> Also: safe as binary or integer?

                        # set 1 for square position in knight bitboard
                        knight_bitboard |= 1 << knight_jump_square
                k += 1
            knight_attack_bitboards[square_nr] = knight_bitboard

            ## ------------------------------------------ ##
            # king moves with bitboards (ignores castling) #
            ## ------------------------------------------ ##

            king_bitboard = 0
            k = 0

            for ofs in direction_offsets:
                king_jump_square = square_nr + ofs
                if is_inside_board(king_jump_square):
                    king_square_y = king_jump_square // 14
                    king_square_x = king_jump_square - king_square_y * 14

                    # make sure no wrap around sides of board
                    max_move_distance = max(abs(x - king_square_x), abs(y - king_square_y))
                    if max_move_distance == 1:
                        king_moves[square_nr][k] = king_jump_square  # TODO: how to deal with empty entries here? -> Also: safe as binary or integer?

                        # set 1 for square position in knight bitboard
                        king_bitboard |= 1 << king_jump_square
                k += 1
            king_attack_bitboards[square_nr] = king_bitboard

            ## -------------------- ##
            # pawn capture bitboards #
            ## -------------------- ##

            pawn_captures_north = []
            pawn_captures_south = []
            pawn_captures_west = []
            pawn_captures_east = []

            # player north
            # if inside_board and no wrap around
            if is_inside_board(square_nr + 13) and abs(x - ((square_nr + 13) % 14)) == 1:
                pawn_captures_north.append(square_nr + 13)
                pawn_attack_bitboards[square_nr][NORTH_INDEX] |= 1 << (square_nr + 13)
            if is_inside_board(square_nr + 15) and abs(x - ((square_nr + 15) % 14)) == 1:
                pawn_captures_north.append(square_nr + 15)
                pawn_attack_bitboards[square_nr][NORTH_INDEX] |= 1 << (square_nr + 15)

            # player south
            if is_inside_board(square_nr - 13) and abs(x - ((square_nr - 13) % 14)) == 1:
                pawn_captures_south.append(square_nr - 13)
                pawn_attack_bitboards[square_nr][SOUTH_INDEX] |= 1 << (square_nr - 13)
            if is_inside_board(square_nr - 15) and abs(x - ((square_nr - 15) % 14)) == 1:
                pawn_captures_south.append(square_nr - 15)
                pawn_attack_bitboards[square_nr][SOUTH_INDEX] |= 1 << (square_nr - 15)

            # player west
            if is_inside_board(square_nr - 13) and abs(x - ((square_nr - 13) % 14)) == 1:
                pawn_captures_west.append(square_nr - 13)
                pawn_attack_bitboards[square_nr][WEST_INDEX] |= 1 << (square_nr - 13)
            if is_inside_board(square_nr + 15) and abs(x - ((square_nr + 15) % 14)) == 1:
                pawn_captures_west.append(square_nr + 15)
                pawn_attack_bitboards[square_nr][WEST_INDEX] |= 1 << (square_nr + 15)

            # player east
            if is_inside_board(square_nr + 13) and abs(x - ((square_nr + 13) % 14)) == 1:
                pawn_captures_east.append(square_nr + 13)
                pawn_attack_bitboards[square_nr][EAST_INDEX] |= 1 << (square_nr + 13)
            if is_inside_board(square_nr - 15) and abs(x - ((square_nr - 15) % 14)) == 1:
                pawn_captures_east.append(square_nr - 15)
                pawn_attack_bitboards[square_nr][EAST_INDEX] |= 1 << (square_nr - 15)

            pawn_attacks_north[square_nr] = pawn_captures_north
            pawn_attacks_south[square_nr] = pawn_captures_south
            pawn_attacks_west[square_nr] = pawn_captures_west
            pawn_attacks_east[square_nr] = pawn_captures_east

            ## -------------------- ##
            # rook capture bitboards #
            ## -------------------- ##

            rook_bitboard = 0

            for direction_index in range(4):
                current_offset = direction_offsets[direction_index]
                for step in range(numSquaresToEdge[square_nr][direction_index]):
                    target_square = square_nr + current_offset * (step + 1)
                    rook_bitboard |= 1 << target_square

            rook_moves[square_nr] = rook_bitboard

            ## ---------------------- ##
            # bishop capture bitboards #
            ## ---------------------- ##

            bishop_bitboard = 0

            for direction_index in range(4, 8, 1):
                current_offset = direction_offsets[direction_index]
                for step in range(numSquaresToEdge[square_nr][direction_index]):
                    target_square = square_nr + current_offset * (step + 1)
                    bishop_bitboard |= 1 << target_square

            bishop_moves[square_nr] = bishop_bitboard

            ## --------------------- ##
            # queen capture bitboards #
            ## --------------------- ##

            queen_moves[square_nr] = rook_moves.get(square_nr) | bishop_moves.get(square_nr)

        else:  # square_nr is dead square
            continue

    ## -------------- ##
    # direction_lookup #
    ## -------------- ##

    # direction_lookup - works like a hashmap for directions between squares
    #   gets called at position: direction_lookup[target_square - start_square + 195]
    #   has twice the board size for positive and negative offsets
    for i in range(392):

        # get the sign
        offset = i - 195

        abs_offset = abs(offset)
        abs_direction = 1  # default left right depending on sign

        if abs_offset % 15 == 0:
            abs_direction = 15
        elif abs_offset % 14 == 0:
            abs_direction = 14
        elif abs_offset % 13 == 0:
            abs_direction = 13

        # python has no sign() function lol
        direction_lookup[i] = abs_direction * -1 if offset < 0 else abs_direction

    ## -------------- ##
    # distance lookup  #
    ## -------------- ##

    # TODO: implement!


def is_inside_board(square_nr):
    """
    checks whether a given square number is within board limits
    """
    return 2 < square_nr < 193 and square_nr not in DEAD_SQUARES


class MoveGenerator:
    moves = []

    def generate_moves(self):
        self.moves.append(Move(None, 75, 89))
        return self.moves









# just for testing
precalculate_data()
print(numSquaresToEdge[73])
print('\n')
print(bin(knight_attack_bitboards.get(190)))
print('\n')
print(knight_moves[75])
print('\n')
print(king_moves[75])
print('\n')
print("Pawn east from 143", pawn_attacks_east[143])
print('\n')
print(bin(pawn_attack_bitboards[75][2]))
print('\n')
print('rook moves', bin(rook_moves.get(3)))
print('\n')
print('queen_moves', bin(queen_moves[3]))
print('\n')
mg = MoveGenerator
print(mg.generate_moves(mg))