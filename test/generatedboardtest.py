import unittest
from generatedboard import *

class TestGeneratedBoard(unittest.TestCase):

    def test_board_size(self):
        generator = GeneratedBoard()
        board = generator.get_board_binary(15, 10)
        self.assertEqual(len(board), 10)
        self.assertEqual(len(board[0]), 15)

    def test_board_many_times(self):
        generator = GeneratedBoard()
        board = generator.get_board_binary(15, 10)
        self.assertEqual(len(board), 10)
        self.assertEqual(len(board[0]), 15)
        board = generator.get_board_binary(10, 15)
        self.assertEqual(len(board), 15)
        self.assertEqual(len(board[0]), 10)
        board = generator.get_board_binary(15, 10)
        self.assertEqual(len(board), 10)
        self.assertEqual(len(board[0]), 15)

    def test_board_is_connected(self):
        generator = GeneratedBoard()
        board = generator.get_board_binary(12, 16)
        builder = Builder(generator.get_board_binary(12, 16), 4)
        builder.board = board
        self.assertTrue(builder.isConnected())
