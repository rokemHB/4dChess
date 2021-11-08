from chess.constants import PLAYERS


class Board:

    square = []

    # starting player
    next_to_move = 0
    current_enemy_players = []

    king_square = dict()

    def __init__(self):
        self.king_square = {'n': 6, 'e': 111, 's': 189, 'w': 84}

    def update_enemy_player(self):
        self.current_enemy_players = [x for x in PLAYERS if x != self.next_to_move]

    def make_move(self):
        pass

        self.next_to_move = PLAYERS[(self.next_to_move + 1) % 4]
