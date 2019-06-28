import unittest
import chessGame

class pathTest(unittest.TestCase):    
    def test_findHorizontalPath(self):
        p1 = (1,8)
        p2 = (8,8)
        expected = [(2,8), (3,8), (4,8), (5,8), (6,8), (7,8)]
        self.assertEqual(chessGame.findStraightPath(p1,p2), expected)

    def test_findHorizontalPathReverse(self):
        p1 = (8,8)
        p2 = (1,8)
        expected = [(7,8), (6,8), (5,8), (4,8), (3,8), (2,8)]
        self.assertEqual(chessGame.findStraightPath(p1,p2), expected)

    def test_findVerticalPath(self):
        p1 = (8,1)
        p2 = (8,8)
        expected = [(8,2), (8,3), (8,4), (8,5), (8,6), (8,7)]
        self.assertEqual(chessGame.findStraightPath(p1,p2), expected)
    
    def test_findVerticalPathDown(self):
        p1 = (8,8)
        p2 = (8,1)
        expected = [(8,7), (8,6), (8,5), (8,4), (8,3), (8,2)]
        self.assertEqual(chessGame.findStraightPath(p1,p2), expected)
    
    def test_diagTest(self):
        p1 = (1,1)
        p2 = (8,8)
        expected = [(2,2), (3,3), (4,4), (5,5), (6,6), (7,7)] 
        self.assertEqual(chessGame.findDiagPath(p1,p2), expected)

    def test_diagDownLeft(self):
        p1 = (8,7)
        p2 = (4,5)
        expected = [(7,6), (6,5), (5,4)]
        self.assertEqual(chessGame.findDiagPath(p1,p2), expected)

    def test_diagUpLeft(self):
        p1 = (5,4)
        p2 = (1,8)
        expected = [(4,5), (3,6), (2,7)]
        self.assertEqual(chessGame.findDiagPath(p1,p2), expected)

    def test_diagUpRight(self):
        p1 = (2,4)
        p2 = (6,8)
        expected = [(3,5), (4,6), (5,7)]
        self.assertEqual(chessGame.findDiagPath(p1,p2), expected)

    def test_diagDownRight(self):
        p1 = (2,7)
        p2 = (7,2)
        expected = [(3,6), (4,5), (5,4), (6,3)]
        self.assertEqual(chessGame.findDiagPath(p1,p2), expected)

if __name__ == '__main__':
    unittest.main()