from chess.constants import PLAYERS
from chess.piece_list import Piece_list


class Board:

    square = []

    # starting player
    next_to_move = 0
    #current_enemy_players = [] TODO: probably not needed

    king_square = dict()

    # piece_lists
    queens = Piece_list()
    rooks = Piece_list()
    bishops = Piece_list()
    knights = Piece_list()


    def __init__(self):
        self.king_square = {'n': 6, 'e': 111, 's': 189, 'w': 84}

    #def update_enemy_player(self):  # TODO: probably not necessary to keep enemys explicitly... n = m[:index] + m[index+1:]
    #    self.current_enemy_players = [x for x in PLAYERS if x != self.next_to_move]

    def make_move(self):
        pass

        self.next_to_move = PLAYERS[(self.next_to_move + 1) % 4]
