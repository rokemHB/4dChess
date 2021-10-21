from abc import ABC, abstractmethod  # Abstract Base Classes¶


class Piece(ABC):
    def __init__(self, square_nr, player):  # player == north || east || south || west
        self.square_nr = square_nr
        self.player = player

    @abstractmethod
    def get_draw_info(self):  # test abstract methods in python
        pass

    def get_square(self):
        return self.square_nr


