import pygame

# Pieces: By en:User:Cburnett - Own workThis W3C-unspecified vector image was created with 
# Inkscape., CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=1499810

class Game:    
    def __init__(self):
        self.pieces = []
        self.objects = []
        self.board_image = pygame.image.load("board.gif")
        self.screen = pygame.display.set_mode((800,800), pygame.RESIZABLE)
        self.selected_piece = None
        self.board_state = {}
        self.turn = 'White'
    

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
    
    def legalMoves(self):
        return Exception("Must be overriden in child class")

    def move(self, posn):
        pass

    def draw(self, screen, location, surface):
        location = (myround(location[0] - 50, 100), myround(location[1] - 50, 100))
        screen.blit(surface, location)

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

    



# TODO: Remove ability to capture forward
# TODO: Add capturing diag 
# TODO: En Passant 
class Pawn(Piece): 
    
    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.hasMoved = False
        self.image = pygame.transform.scale(pygame.image.load(color + "_pawn.PNG"), (100,100))

    # return true if the piece can move to that location, false if not
    def legalMove(self, location, game):
        x_dist = location[0] - self.coord[0]
        y_dist = location[1] - self.coord[1]
        dist = x_dist + y_dist
        if self.color != game.turn:
            return False
        if self.color == 'White':
            if self.hasMoved == False:
                if x_dist == 0 and (y_dist == 1 or y_dist == 2):
                    self.hasMoved = True
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
            if self.hasMoved == False:
                if x_dist == 0 and (y_dist == -1 or y_dist == -2):
                    self.hasMoved = True
                    return True
                else: 
                    return False 
            else:
                if x_dist == 0 and y_dist == -1:
                    return True
                else:
                    return False
                             
    
    def promote(self):
        pass

    def findPath(self, start, end):
        return findStraightPath(start,end)    

class Rook(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load(color + "_rook.PNG"), (100,100))
    # return true if moving to the given coord is legal 
    def legalMove(self, coord, game):
        if self.color != game.turn:
            return False
        if coord[0] != self.coord[0] and coord[1] != self.coord[1]:
            return False
        else:
            return True
        
    def move(self):
        pass

    def findPath(self, start, end):
        return findStraightPath(start, end)    


class Knight(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load(color + "_knight.PNG"), (100,100))

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

    def move(self):
        pass

    def findPath(self, start, end):
        return []    

class Bishop(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load(color + "_bishop.PNG"), (100,100))


    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self,coord, game):
        if self.color != game.turn:
            return False
        x_dist = abs(self.coord[0] - coord[0])
        y_dist = abs(self.coord[1] - coord[1])
        if (x_dist == y_dist):
            return True
        return False 

    def move(self):
        pass
    
    def findPath(self, start, end):
        return findDiagPath(start,end)

class Queen(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load(color + "_queen.PNG"), (100,100))

    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self, coord, game):
        if self.color != game.turn:
            return False
        r = Rook(self.color, self.posn)
        b = Bishop(self.color, self.posn)
        if (r.legalMove(coord,game) or b.legalMove(coord,game)):
            return True
        return False

    def move(self):
        pass
    
    def findPath(self, start, end):
        if start[0] != end[0] and start[1] != end[1]:
            return findDiagPath(start, end)

        else:
            return findStraightPath(start,end) 

# TODO: Castling 
class King(Piece):
    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load(color + "_king.PNG"), (100,100))
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
                castleWhite(self, game)  
        # Black
        else:
            if self.canCastle and self.coord == (5,8) and (coord == (7,8) or coord == (3,8)):
                castleBlack(self,game)
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
     
    # main loop
    while running:

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            pygame.display.update()
            updateBoard(g, board)
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
                        updateBoard(g, board)
                        g.selected_piece = None
                
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

# if this piece can move to that position, move it there 
def updatePiecePosition(g, piece, to_square):
    coord = findCoord(to_square)
    if piece.teammateOnSquare(coord,g):
        return False
    if piece.legalMove(coord, g):
        path = piece.findPath(piece.coord, coord)
        print(path)
        for place in path:
            if piece.teammateOnSquare(place,g):
                print("Teamate piece in the way!")
                return False
            if piece.pieceOnSquare(place,g):
                print("Enemy piece in the way!")
                return False    
        checkCapture(coord, g)
        piece.posn = to_square
        del g.board_state[piece.coord]
        piece.coord = coord        
        g.board_state[coord] = piece 
        return True
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
def checkCapture(coord, g):
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

def castleWhite(king, game):
    print("Castle White!")

def castleBlack(king, game):
    print("Castle Black!")    

main()


     