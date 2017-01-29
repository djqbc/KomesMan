import unittest
from binaryboarditemsgetter import *

class TestBinaryBoardItemsGetter(unittest.TestCase):
    def test_items(self):
        getter = BinaryBoardItemsGetter()
        board = [[4, 5],
                 [2, 3]]
        getter.load_items(board)
        self.assertEqual(len(getter.pills), 1)
        self.assertEqual(len(getter.caps), 1)
        self.assertEqual(len(getter.beers), 1)
        self.assertEqual(len(getter.amphs), 1)
        