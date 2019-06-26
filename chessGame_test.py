import unittest
import chessGame

class basicTest(unittest.TestCase):    
    def test_findHorizontalPath(self):
        p1 = (1,8)
        p2 = (8,8)
        expected = [(2,8), (3,8), (4,8), (5,8), (6,8), (7,8)]
        self.assertEqual(chessGame.findStraightPath(p1,p2), expected)
    def test_findVerticalPath(self):
        p1 = (8,1)
        p2 = (8,8)
        expected = [(8,2), (8,3), (8,4), (8,5), (8,6), (8,7)]

if __name__ == '__main__':
    unittest.main()