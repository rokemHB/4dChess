import unittest
from unittest import TestCase

import pygame

from chess.board import Board
from chess.pieces.king import King
from chess.pieces.pawn import Pawn
from chess.pieces.rook import Rook


class TestPieces(TestCase):

    board = Board()
    WIN = pygame.display.set_mode((100, 100))

    testPawn = Pawn(118, 'w')

    startPositions = [
        Rook(105, 'e'), King(103, 'w'), testPawn
    ]

    def setUp(self):
        for piece in self.startPositions:
            self.board.set_piece(piece.get_square(), piece)
        self.board.load_images(path="../chess/images/")

    # TODO test if this is necessary
    def tearDown(self):
        board = Board()

    # Pawn allowed to walk even though it muss kill rook that sets own King in check!
    def test_move_only_to_kill_piece_setting_me_check(self):
        self.board.selected_piece = self.board.get_piece(118)  # select the pawn
        self.board.make_move(self.board.get_coordinates_from_square_nr(119), self.WIN)
        self.assertFalse(self.board.get_piece(119), self.testPawn)


