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
    




class Pawn(Piece): 
    
    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.hasMoved = False
        self.image = pygame.transform.scale(pygame.image.load("White_pawn.PNG"), (100,100))

    # return true if the piece can move to that location, false if not
    def legalMove(self, location):
        if self.hasMoved == False:
            if location[1] - self.coord[1] == 2 or location[1] - self.coord[1] == 1:
                self.hasMoved = True
                return True
            else: 
                return False 
        else:
            if location[1] - self.coord[1] == 1:
                return True
            else:
                return False         
    
    def promote(self):
        pass

class Rook(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("White_rook.PNG"), (100,100))

    # return true if moving to the given coord is legal 
    def legalMove(self, coord):
        if coord[0] != self.coord[0] and coord[1] != self.coord[1]:
            return False
        else:
            return True
        
    def move(self):
        pass


class Knight(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("White_knight.PNG"), (100,100))

    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self,coord):
        pass

    def move(self):
        pass

class Bishop(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("White_bishop.PNG"), (100,100))


    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMove(self,coord):
        if (self.coord[0] == coord[0] or self.coord[1] == coord[1]):
            return False
        return True 

    def move(self):
        pass

class Queen(Piece):

    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("White_queen.PNG"), (100,100))

    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMoves(self):
        pass

    def move(self):
        pass

class King(Piece):
    def __init__(self, color, posn):
        super().__init__(color, posn)
        self.image = pygame.transform.scale(pygame.image.load("White_king.PNG"), (100,100))

    # return a list of tuples with the coordinates of legal moves for this piece
    def legalMoves(self):
        pass

    def move(self):
        pass


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
                        g.selected_piece = findClosestPiece(g,click)
                    else:
                        to_square = (myround(event.pos[0], 50), myround(event.pos[1], 50))
                        updatePiecePosition(g.selected_piece, to_square)
                        updateBoard(g, board)
                        g.selected_piece = None
                
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

# draw all of the pieces and the board
def updateBoard(g, board):
    board.draw(g.screen)
    for p in g.pieces:
        p.draw(g.screen, p.posn, p.image)
    pygame.display.update()    

# if this piece can move to that position, move it there 
def updatePiecePosition(piece, from_square):
    coord = findCoord(from_square)
    if piece.legalMove(coord):
        piece.posn = from_square
        piece.coord = coord
    

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

def myround(x, base):
    return base * round(x/base)

# given mouse location find the closest piece to that location
# if we didn't click close enough to a piece return nothing 
def findClosestPiece(g,mouse):
    for p in g.pieces:
        if (eucDist(mouse, p.posn) < 50):
            return p


# basic Euclidean distance
def eucDist(pos1, pos2):
    dist = ((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)**.5
    return dist

# given a posn return it's coordinates on the chess board
def findCoord(posn):
    return ((posn[0] + 50) // 100 , 8 - (posn[1] + 50) // 100 + 1)


main()


     