from square import *
from piece import *
from color import *
from force import *
from engine import *
#import keyboard

class BoardController():

    def __init__(self, controller):

        self.controller = controller

        self.engine = Engine()
        self.board = None
        self.selector = None

        self.selector_selected_piece = None
        self.selector_selected_color = None

        self.board_selected_square = None

        self.board_data = {
            Square.A1: None,
            Square.A2: None,
            Square.A3: None,

            Square.B1: None,
            Square.B2: None,
            Square.B3: None,

            Square.C1: None,
            Square.C2: None,
            Square.C3: None
        }

    def get_fen(self, color):

        rank1 = self.get_fen_rank(Square.A1, Square.B1, Square.C1)
        rank2 = self.get_fen_rank(Square.A2, Square.B2, Square.C2)
        rank3 = self.get_fen_rank(Square.A3, Square.B3, Square.C3)

        if color == Color.white:
            return "8/8/8/8/8/"+rank3+"/"+rank2+"/"+rank1+" w - - 0 1"
        else:
            return "8/8/8/8/8/"+rank3+"/"+rank2+"/"+rank1+" b - - 0 1"


    def get_fen_rank(self, a, b, c):
        if self.board_data[a] == None and self.board_data[b] != None and self.board_data[c] != None:
            return "1" + self.getCasedPiece(b) + self.getCasedPiece(c) + "5"
        if self.board_data[a] != None and self.board_data[b] == None and self.board_data[c] != None:
            return self.getCasedPiece(a) + "1" + self.getCasedPiece(c) + "5"
        if self.board_data[a] != None and self.board_data[b] != None and self.board_data[c] == None:
            return self.getCasedPiece(a) + self.getCasedPiece(b) + "6"

        if self.board_data[a] == None and self.board_data[b] == None and self.board_data[c] != None:
            return "2"+ self.getCasedPiece(c) + "5"
        if self.board_data[a] == None and self.board_data[b] != None and self.board_data[c] == None:
            return "1" + self.getCasedPiece(b) + "6"
        if self.board_data[a] != None and self.board_data[b] == None and self.board_data[c] == None:
            return self.getCasedPiece(a) + "7"

        if self.board_data[a] != None and self.board_data[b] != None and self.board_data[c] != None:
            return self.getCasedPiece(a) + self.getCasedPiece(b) + self.getCasedPiece(c) + "5"
        
        return "8"

    def selector_clicked(self, piece: Piece, color: Color):
        if (self.selector == None): return

        # if a square is marked on the board
        if (self.board_selected_square != None):
            self.board.demark(self.board_selected_square)
            self.place(piece, color, self.board_selected_square)
            self.board_selected_square = None
            return

        # if you mark another piece in the selector
        if (self.selector_selected_piece != None and self.selector_selected_color != None):
            self.selector.demark(self.selector_selected_piece, self.selector_selected_color)
        
        # demark if same selected again
        if (self.selector_selected_piece == piece and self.selector_selected_color == color):
            self.selector_selected_color = None
            self.selector_selected_piece = None
            self.selector.demark(self.selector_selected_piece, self.selector_selected_color)
            return

        self.selector_selected_color = color
        self.selector_selected_piece = piece
        self.selector.mark(piece, color)

    def mark(self, square: Square):
        self.board.mark(square)

        if self.board_data[square] != None:

            self.applyForces(square)

    def board_clicked(self, square: Square):
        # if a piece is about to be placed
        if (self.selector_selected_piece != None and self.selector_selected_color != None):
            self.place(self.selector_selected_piece, self.selector_selected_color, square)
            self.selector.demark(self.selector_selected_piece, self.selector_selected_color)
            self.selector_selected_color = None
            self.selector_selected_piece = None
            return
        
        # if selecting a piece on the board to move, or moving selection
        if (self.board_selected_square == None):
            self.board_selected_square = square
            self.mark(square)
            return

         # if deselecting
        if (self.board_selected_square == square):
            self.board.demark(self.board_selected_square)
            self.board_selected_square = None
            
            if self.board_data[square] != None:
                self.clearForces()
            return

        # if moving selection
        if (not self.occupied(self.board_selected_square)):
            self.board.demark(self.board_selected_square)
            self.board.mark(square)
            self.board_selected_square = square
            self.clearForces()
            return
        
        # if performing a move
        self.move(self.board_selected_square, square)
        self.board_selected_square = None
        self.clearForces()

    def applyForces(self, fromSquare: Square, onlyOnSqaure: Square = None):
        fen = self.get_fen(self.getColor(fromSquare))
       
        tKing = None
        oKing = None
        for square in self.board_data:
            if self.board_data[square] == None:
                continue

            color = self.board_data[square]['color']
            piece = self.board_data[square]['piece']

            if piece == Piece.K:
                if color != self.getColor(fromSquare):
                    oKing = str(square).split(".")[1].lower()
                elif color == self.getColor(fromSquare):
                    tKing = str(square).split(".")[1].lower()
        
        if oKing == None or tKing == None:
            return

        ratings = self.engine.rateSquares(fen, str(fromSquare).split(".")[1].lower(), oKing)
        
        def force(square):
            fromColor = self.getColor(fromSquare)
            toColor = self.getColor(square)

            # hvis modsat farve
            if toColor != None and toColor != fromColor:
                return Force.neutral

            if fromColor != toColor:
                return ratings[str(square).split(".")[1].lower()]
            else:
                return Force.neutral
        
        def led(square):
            return True if ratings[str(square).split(".")[1].lower()] != Force.push else False

        if onlyOnSqaure == None:
            for square in Square:
                self.board.setForce(square, force(square))
                self.controller.setForce(square, force(square))
                self.board.attackable(led(square), square)
                self.controller.setLed(square, led(square))
        else:
            self.board.setForce(onlyOnSqaure, force(onlyOnSqaure))
            self.controller.setForce(onlyOnSqaure, force(onlyOnSqaure))
            self.board.attackable(led(onlyOnSqaure), onlyOnSqaure)
            self.controller.setLed(onlyOnSqaure, led(onlyOnSqaure))

    def clearForces(self):
        for square in Square:
            self.board.setForce(square, Force.neutral)
            self.controller.setForce(square, Force.neutral)
            self.board.attackable(False, square)
            self.controller.setLed(square, False)


    def move(self, fromSquare: Square, toSquare: Square):
        occupied, color, piece = self.get(fromSquare)
        if (occupied == False): 
            return

        self.board.demark(fromSquare)
        self.clear(fromSquare)
        self.place(piece, color, toSquare)

    def clear(self, square: Square):
        self.board_data[square] = None
        self.board.clear(square)

    def occupied(self, square: Square):
        o, _, _ = self.get(square)
        return o

    def get(self, square: Square):
        color = self.getColor(square)
        piece = self.getPiece(square)
        if (piece == None or color == None):
            return False, None, None
        else:
            return True, color, piece
    
    def getCasedPiece(self, square: Square):
        data = self.board_data[square]
        return data["piece"].value if data['color'] == Color.white else data["piece"].value.lower()

    def getColor(self, square: Square):
        data = self.board_data[square]
        if (data == None):
            return None
        else: return data["color"]

    def getPiece(self, square: Square):
        data = self.board_data[square]
        if (data == None):
            return None
        else: return data["piece"]

    def place(self, piece: Piece, color: Color, square: Square):
        self.board.place(piece, color, square)
        self.board_data[square] = {
            "piece": piece,
            "color": color
        }

    def clearAll(self):
        for square in Square:
            self.clear(square)
            
    
    def reset(self):
        self.clearAll()
        self.clearForces()
        self.board.demark(self.board_selected_square)

        self.board_selected_square = None

        self.selector_selected_piece = None
        self.selector_selected_color = None