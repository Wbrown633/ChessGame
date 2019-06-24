import pygame

# Pieces: By en:User:Cburnett - Own workThis W3C-unspecified vector image was created with 
# Inkscape., CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499810

class Game:    
    def __init__(self):
        self.pieces = []
        self.objects = []
        self.board_image = pygame.image.load("Resources/board.gif")
        self.screen = pygame.display.set_mode((1000,800), pygame.RESIZABLE)
        self.selected_piece = None
        self.board_state = {}
        self.turn = 'White'
        self.enPassantWhite = None
        self.enPassantBlack = None
        self.whiteInCheck = False
        self.blackInCheck = False
    

class Board:   

    def __init__(self, board_image, height, width):
        self.height = height
        self.width = width
        self.board_scale = pygame.transform.scale(board_image, (height, width))

    def draw(self, screen):
        screen.blit(self.board_scale, (0,0))


class Piece:
    """Abstract base class all pieces inherit from"""  

    def __init__ (self, color, posn):
        self.color = color # set the color of this piece 
        self.posn = posn # set the starting posn of this piece
        self.coord = findCoord(posn) # starting coord calculated based on starting posn
    
    def pieceType(self):
        return type(self).__name__

    def draw(self, screen, location, surface):
        location = (myround(location[0] - 50, 100), myround(location[1] - 50, 100))
        screen.blit(surface, findPosn(self.coord))

    # return true if this piece has a teammate piece on the given square
    def teammateOnSquare(self, coord, game):
        if coord in game.board_state:
            piece_on_square = game.board_state[coord]
            if piece_on_square.color == self.color:
                return True
        return False
    
    def pieceOnSquare(self, coord, game):
        if coord in game.board_state:
            return True
        return False

    def legalMove(self, coord):
        pass

    # Return true if this piece can capture that piece
    def canCapture(self, piece, game):
        # Can't capture teammates
        if self.color == piece.color:
            return False

        if self.legalMove(piece.coord):
            if pieceInPath(piece, game, piece.coord) == False or self.pieceType == "Knight":
                return True
        return False
    
    # move this piece to_square
    def move(self, to_square, g):
        coord = findCoord(to_square)
        self.posn = to_square
        del g.board_state[self.coord]
        self.coord = coord        
        g.board_state[coord] = self

class Pawn(Piece): 
    
    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.hasMoved = False
        self.image = pygame.transform.scale(pygame.image.load("Resources/" + color + "_pawn.PNG"), (100,100))

    # return true if the piece can move to that location, false if not
    def legalMove(self, location, game):
        x_dist = location[0] - self.coord[0]
        y_dist = location[1] - self.coord[1]
        dist = x_dist + y_dist

        # can't move out of turn
        if self.color != game.turn:
            return False

        # cannot move through pieces
        if location in game.board_state and x_dist == 0:
            return False

        # capture diagonally 
        if abs(x_dist) == 1 and abs(y_dist) == 1 and location in game.board_state:
            piece = game.board_state[location]
            if piece.color != self.color:
                self.hasMoved = True
                return True

        if self.color == 'White':
            # Capture en passant
            if game.enPassantBlack == location:
                if abs(x_dist) == 1 and abs(y_dist) == 1:
                    del game.board_state[(location[0], location[1] - 1)]
                    return True
            if self.hasMoved == False:
                if x_dist == 0 and (y_dist == 1 or y_dist == 2):
                    self.hasMoved = True
                    game.enPassantWhite = (location[0], location[1] - 1)
                    return True
                else: 
                    return False 
            else:
                if x_dist == 0 and y_dist == 1:
                    return True
                else:
                    return False
        # move logic for black pawns 
        else:
            # Capture en passant
            if game.enPassantWhite == location:
                if abs(x_dist) == 1 and abs(y_dist) == 1:
                    del game.board_state[(location[0], location[1] + 1)]
                    return True
            if self.hasMoved == False:
                if x_dist == 0 and (y_dist == -1 or y_dist == -2):
                    self.hasMoved = True
                    game.enPassantBlack = (location[0], location[1] + 1)
                    return True
                else: 
                    return False 
            else:
                if x_dist == 0 and y_dist == -1:
                    return True
                else:
                    return False
                             
    # TODO: Allow under promotion
    def promote(self, game, coord):
        # delete the pawn
        del game.board_state[self.coord]

        # take the piece if we're moving onto one 
        if coord in game.board_state:
            del game.board_state[coord]
        # add the queen
        game.board_state[coord] = Queen(self.color, findPosn(coord))


    def findPath(self, start, end):
        return findStraightPath(start,end)    

class Rook(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("Resources/" + color + "_rook.PNG"), (100,100))
    # return true if moving to the given coord is legal 
    def legalMove(self, coord, game):
        if self.color != game.turn:
            return False
        if coord[0] != self.coord[0] and coord[1] != self.coord[1]:
            return False
        else:
            return True

    def findPath(self, start, end):
        return findStraightPath(start, end)    


class Knight(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("Resources/" + color + "_knight.PNG"), (100,100))

    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self,coord,game):
        if self.color != game.turn:
            return False
        x_dist = abs(self.coord[0] - coord[0])
        y_dist = abs(self.coord[1] - coord[1])
        dist = x_dist + y_dist
        if (dist == 3 and (x_dist == 1 or y_dist == 1)):
            return True
        return False

    def findPath(self, start, end):
        return []    


class Bishop(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("Resources/" + color + "_bishop.PNG"), (100,100))


    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self,coord, game):
        if self.color != game.turn:
            return False
        x_dist = abs(self.coord[0] - coord[0])
        y_dist = abs(self.coord[1] - coord[1])
        if (x_dist == y_dist):
            return True
        return False 

    def findPath(self, start, end):
        return findDiagPath(start,end)

class Queen(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("Resources/" + color + "_queen.PNG"), (100,100))

    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self, coord, game):
        if self.color != game.turn:
            return False
        r = Rook(self.color, self.posn)
        b = Bishop(self.color, self.posn)
        if (r.legalMove(coord,game) or b.legalMove(coord,game)):
            return True
        return False
    
    def findPath(self, start, end):
        if start[0] != end[0] and start[1] != end[1]:
            return findDiagPath(start, end)

        else:
            return findStraightPath(start,end) 

# TODO: Implement Check and Checkmate
# TODO: Prevent user from castling into or out of check
# TODO: Preven user from moving a piece if it puts them in check 

class King(Piece):
    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("Resources/" + color + "_king.PNG"), (100,100))
        self.canCastle = True

    # return true if this piece can move to the given coord 
    def legalMove(self, coord, game):
        if self.color != game.turn:
            return False
        x_dist = abs(self.coord[0] - coord[0])
        y_dist = abs(self.coord[1] - coord[1])
        dist = x_dist + y_dist

        # Castling rules
        # White
        if self.color == 'White':
            if self.canCastle and self.coord == (5,1) and (coord == (7,1) or coord == (3,1)):
                castleWhite(self, coord, game)  
        # Black
        else:
            if self.canCastle and self.coord == (5,8) and (coord == (7,8) or coord == (3,8)):
                castleBlack(self, coord, game)
        if (dist == 1):
            return True
        elif (dist == 2):
            if (x_dist == 1):
                return True
        return False

    def findPath(self, start, end):
        return []    


# define a main function
def main():
    
    g = Game()
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("CHESS")
    board = Board(g.board_image, 800,800)
    addPieces(g)
    

    # define a variable to control the main loop
    running = True
    updateBoard(g, board)
    pygame.display.update()
    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            
            # click to move pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if g.selected_piece == None:
                        click = event.pos
                        coord = findCoord(click)
                        if coord in g.board_state:
                            g.selected_piece = g.board_state[coord]
                    else:
                        to_square = (myround(event.pos[0], 50), myround(event.pos[1], 50))
                        if updatePiecePosition(g, g.selected_piece, to_square):
                            nextTurn(g)
                        g.selected_piece = None
                    updateBoard(g, board)
                    pygame.display.update()  
                
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

# draw all of the pieces and the board
def updateBoard(g, board):
    board.draw(g.screen)
    for coord in g.board_state:
        p = g.board_state[coord]
        p.draw(g.screen, p.posn, p.image)
    pygame.display.update()
    f = pygame.font.Font(None, 40)
    s = f.render(g.turn, True, [0, 0, 0], [255, 255, 255])
    white = f.render("White King", True, [0,0,0], [255, 255, 255])
    black = f.render("Black King", True, [0,0,0], [255, 255, 255])
    w1 = f.render("in Check: " + str(g.whiteInCheck), True, [0,0,0], [255, 255, 255])
    b1 = f.render("in Check: " + str(g.blackInCheck), True, [0,0,0], [255, 255, 255])
    g.screen.blit(s, (800,350))
    g.screen.blit(white, (800, 450))
    g.screen.blit(w1, (800, 475))
    g.screen.blit(black, (800, 550))
    g.screen.blit(b1, (800, 575))

# if this piece can move to that position, move it there 
def updatePiecePosition(g, piece, to_square):
    coord = findCoord(to_square)
    if piece.teammateOnSquare(coord,g):
        return False
    if piece.legalMove(coord, g):
        if piece.pieceType() == 'Pawn' and (coord[1] == 1 or coord[1] == 8):
            piece.promote(g, coord)
            return True
        if pieceInPath(piece, g, to_square):
            return False          
        capture(coord, g)
        piece.move(to_square, g)         
        return True
    return False    
    
# return True if there is a piece (enemy or teammate) that is in the way
def pieceInPath(piece, g, to_square):
    path = piece.findPath(piece.coord, to_square)
    for place in path:
        if piece.teammateOnSquare(place,g):
            print("Teamate piece in the way!")
            return False
        if piece.pieceOnSquare(place,g):
            print("Enemy piece in the way!")
            return False 

def addPieces(g):
    for x in range(8):
        g.pieces.append(Pawn('White', (50 + x * 100,650)))
    g.pieces.append(Rook('White', (50, 750)))
    g.pieces.append(Knight('White', (150, 750)))
    g.pieces.append(Bishop('White', (250, 750)))
    g.pieces.append(Queen('White', (350, 750)))
    g.pieces.append(King('White', (450, 750)))
    g.pieces.append(Bishop('White', (550, 750)))
    g.pieces.append(Knight('White', (650, 750)))    
    g.pieces.append(Rook('White', (750, 750)))
    for x in range(8):
        g.pieces.append(Pawn('Black', (50 + x * 100,150)))
    g.pieces.append(Rook('Black', (50, 50)))
    g.pieces.append(Knight('Black', (150, 50)))
    g.pieces.append(Bishop('Black', (250, 50)))
    g.pieces.append(Queen('Black', (350, 50)))
    g.pieces.append(King('Black', (450, 50)))
    g.pieces.append(Bishop('Black', (550, 50)))
    g.pieces.append(Knight('Black', (650, 50)))    
    g.pieces.append(Rook('Black', (750, 50)))
    for p in g.pieces:
        g.board_state[p.coord] = p

def myround(x, base):
    return base * round(x/base)

# basic Euclidean distance
def eucDist(pos1, pos2):
    dist = ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)**.5
    return dist

# given a posn return it's coordinates on the chess board
def findCoord(posn):
    return ((posn[0]) // 100 + 1, 8 - (posn[1]) // 100 )

# change the color of the turn
def nextTurn(game):
    if game.turn == 'White':
        game.turn = 'Black'
    else:
        game.turn = 'White'

# capture a piece on this square if we land there 
def capture(coord, g):
    if coord in g.board_state:
        del g.board_state[coord]

# return a list of posn between this location and that on a straight line
def findStraightPath(start, end):
    listofCoords = []

    # Horizontal Line
    if start[1] == end[1]:
        # move left
        if start[0] > end[0]:
            while start[0] > end[0] + 1:
                start = (start[0] - 1, start[1])
                listofCoords.append(start)

        # move right
        else:
            while start[0] < end[0] - 1:
                start = (start[0] + 1, start[1])
                listofCoords.append(start)

    # Vertical Line
    else:
        # move up 
        if start[1] < end[1]:
            while start[1] < end[1] - 1:
                start = (start[0], start[1] + 1)
                listofCoords.append(start)

        # move down
        else:
            while start[1] > end[1] + 1:
                start = (start[0], start[1] - 1)
                listofCoords.append(start)
    return listofCoords

# return a list of posn between this location and that on diagonal line
def findDiagPath(start, end):
    listofCoords = []    
    if start[1] < end[1]:
        # up and to the left
        if start[0] > end[0]:
            while start[0] > end[0] + 1:
                start = (start[0] - 1, start[1] + 1)
                listofCoords.append(start)

        # up and to the right
        else:
            while start[0] < end[0] - 1:
                start = (start[0] + 1, start[1] + 1)
                listofCoords.append(start)

    if start[1] > end[1]:

        # down and to the left
        if start[0] > end[0]:
            while start[0] > end[0] + 1:
                start = (start[0] - 1, start[1] - 1)
                listofCoords.append(start)
        # down and to the right
        else:
            while start[0] < end[0] - 1:
                start = (start[0] + 1, start[1] - 1)
                listofCoords.append(start)

    return listofCoords

def castleWhite(king, coord, game):
    # Kingside
    if coord[0] > king.coord[0]:
        king.coord = (7,1)
        king.posn = (650, 750)
        rook = game.board_state[(8,1)]
        rook.coord = (6,1)
        rook.posn = (550, 750)
        board = game.board_state
        del board[(5,1)]
        del board[(8,1)]
        board[(7,1)] = king
        board[(6,1)] = rook
        print("Castle Kingside White!")
    # Queenside
    else:

        king.coord = (3,1)
        king.posn = (250, 750)
        rook = game.board_state[(1,1)]
        rook.coord = (4,1)
        rook.posn = (350, 750)
        board = game.board_state
        del board[(5,1)]
        del board[(1,1)]
        board[(3,1)] = king
        board[(4,1)] = rook
        print("Castle Queenside White!")
    king.canCastle = False
    game.turn = 'Black'


def castleBlack(king, coord, game):
    # Kingside
    if coord[0] > king.coord[0]:
        king.coord = (7,8)
        king.posn = (650, 50)
        rook = game.board_state[(8,8)]
        rook.coord = (6,8)
        rook.posn = (550, 50)
        board = game.board_state
        del board[(5,8)]
        del board[(8,8)]
        board[(7,8)] = king
        board[(6,8)] = rook
        print("Castle Kingside Black!")
    # Queenside
    else:
        king.coord = (3,8)
        king.posn = (250, 50)
        rook = game.board_state[(1,8)]
        rook.coord = (4,8)
        rook.posn = (350, 50)
        board = game.board_state
        del board[(5,8)]
        del board[(1,8)]
        board[(3,8)] = king
        board[(4,8)] = rook
        print("Castle Queenside Black!") 
    king.canCastle = False
    game.turn = 'White'    

def findPosn(coord):

    posn = (coord[0] * 100 - 100, abs(coord[1]-8) * 100)
    return posn


main()


     