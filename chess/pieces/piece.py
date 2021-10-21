from abc import ABC, abstractmethod  # Abstract Base Classes¶


class Piece(ABC):
    def __init__(self, squareNr, player):  # player == north || east || south || west
        self.squareNr = squareNr
        self.player = player

    @abstractmethod
    def get_draw_info(self):  # test abstract methods in python
        pass
