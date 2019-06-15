import unittest
import chessGame

class basicTest(unittest.TestCase):
    def test_def(self):
        r = chessGame.Rook('White', (50,50))
        self.assertFalse(r.legalMove((100,100)))
