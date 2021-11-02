from unittest import TestCase

import pygame

from chess.board import Board
from chess.pieces.king import King
from chess.pieces.pawn import Pawn
from chess.pieces.rook import Rook


class TestPieces(TestCase):

    board = Board()
    WIN = pygame.display.set_mode((100, 100))

    def setUp(self):
        board = Board()
        self.board.load_images(path="../chess/images/")

    def test_move_only_to_kill_piece_setting_me_check(self):
        # Pawn must not be allowed to walk, must kill rook that sets own King in check!
        testPawn = Pawn(118, 'w')

        startPositions = [
            Rook(105, 'e'), King(103, 'w'), testPawn
        ]
        for piece in startPositions:
            self.board.set_piece(piece.get_square(), piece)
        self.board.selected_piece = self.board.get_piece(118)  # select the pawn
        self.board.make_move(get_coordinates_from_square_nr(119), self.WIN)
        self.assertFalse(self.board.get_piece(119) == testPawn)
        self.assertTrue(self.board.get_piece(118) == testPawn)

    def test_king_updates_position_internally(self):
        # King just makes simple step, compares if board class updates position correctly
        self.board.set_piece(3, King(3, 'n'))
        self.board.selected_piece = self.board.get_piece(3)
        self.board.king_pos['n'] = 3
        self.board.click(get_coordinates_from_square_nr(3), 'n', self.WIN)  # click needed to fill move_list
        self.board.make_move(get_coordinates_from_square_nr(17), self.WIN)
        self.assertTrue(self.board.king_pos.get('n') == 17)

    def test_king_moves_when_in_check(self):
        test_piece = King(75, 'n')
        self.board.set_piece(75, test_piece)
        self.board.king_pos['n'] = 75
        self.board.set_piece(103, Rook(103, 'w'))
        self.board.click(get_coordinates_from_square_nr(75), 'n', self.WIN)  # click needed to fill move_list
        # illegal move
        self.board.make_move(get_coordinates_from_square_nr(89), self.WIN)
        self.assertTrue(self.board.get_piece(75) == test_piece)
        self.assertTrue(self.board.get_piece(89) is None)
        # legal move
        self.board.make_move(get_coordinates_from_square_nr(90), self.WIN)
        self.assertTrue(self.board.get_piece(90) == test_piece)
        self.assertTrue(self.board.get_piece(75) is None)


