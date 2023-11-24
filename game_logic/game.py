from .literals import *
from .helpers import *
from .piece import *
import pygame, copy

class Game:
    def __init__(self, playerCount=3):
        if playerCount in (2,3): self.playerCount = playerCount
        else: self.playerCount = 3
        self.pieces: dict[int, set[Piece]] = {1:set(), 2:set(), 3:set()}
        self.board = self.createBoard(playerCount)
        #for drawing board
        self.unitLength = int(WIDTH * 0.05) #unitLength length in pixels
        self.lineWidth = int(self.unitLength * 0.05) #line width
        self.circleRadius = int(HEIGHT * 0.025) #board square (circle) radius
        self.centerCoor = (WIDTH/2, HEIGHT/2) #window size is 800*600

    def createBoard(self, playerCount: int):
        Board = {}
        #player 1 end zone
        for p in range(-4,1):
            for q in range(4,9):
                if p + q > 4: continue
                else: 
                    if (p,q) not in Board: Board[(p,q)] = None
        #player 1 start zone
        for p in range(0,5):
            for q in range(-8,-3):
                if p + q < -4: continue
                else: 
                    Board[(p,q)] = Piece(1, p, q)
                    self.pieces[1].add(Board[p, q])
        #player 2 end zone
        for p in range(4,9):
            for q in range(-4,1):
                if p + q > 4: continue
                else: 
                    if (p,q) not in Board: Board[(p,q)] = None
        #player 2 start zone
        for p in range(-8,-3):
            for q in range(0,5):
                if p + q < -4: continue
                else: 
                    Board[(p,q)] = Piece(2, p, q)
                    self.pieces[2].add(Board[p, q])
        #player 3 end zone
        for p in range(-4,1):
            for q in range(-4,1):
                if p + q > -4: continue
                else:
                    if (p,q) not in Board: Board[(p,q)] = None
        #player 3 start zone
        for p in range(0,5):
            for q in range(0,5):
                if p + q < 4: continue
                else:
                    Board[(p,q)] = None if playerCount == 2 else Piece(3, p, q)
                    if playerCount == 3: self.pieces[3].add(Board[p, q])
        #neutral zone
        for p in range(-3,4):
            for q in range(-3,4):
                if p + q <= 3 and p + q >= -3: Board[(p,q)] = None
        return Board

    def getValidMoves(self, startPos: tuple, playerNum: int):
        '''Inputs the piece's starting position, playing player's number, and `self.board`.
        Returns a `list` of objective coordinates of valid moves (end coordinates) that piece can make.'''
        moves = []
        for direction in DIRECTIONS:
            destination = add(startPos, direction)
            if destination not in self.board: continue #out of bounds
            elif self.board[destination] == None: moves.append(destination) #walk
            else: #self.board[destination] != None
                destination = add(destination, direction)
                if destination not in self.board or self.board[destination] != None: continue #out of bounds or can't jump
                moves.append(destination)
                checkJump(moves, self.board, destination, direction, playerNum)
        for i in copy.deepcopy(moves):
            #You can move past other player's territory, but you can't stay there.
            if (i not in START_COOR[playerNum]) and (i not in END_COOR[playerNum]) and (i not in NEUTRAL_COOR):
                while i in moves:
                    moves.remove(i)
        return list(set(moves))

    def checkWin(self, playerNum: int):
        for i in END_COOR[playerNum]:
            if self.board[i] == None: return False
            if isinstance(self.board[i], Piece) and self.board[i].getPlayerNum() != playerNum: return False
        return True

    def getBoardState(self, playerNum: int):
        '''Key: subjective coordinates\nValue: piece's player number, or 0 if it's vacant'''
        state = dict()
        for i in self.board:
            state[obj_to_subj_coor(i, playerNum)] = (0 if self.board[i] == None else int(self.board[i].getPlayerNum()))
        return state
    
    def getBoolBoardState(self, playerNum: int):
        '''Key: subjective coordinates\nValue: `true`, or `false` if it's vacant'''
        state = dict()
        for i in self.board:
            state[obj_to_subj_coor(i, playerNum)] = (self.board[i] != None)
        return state

    def allMovesDict(self, playerNum: int):
        '''Returns a dict of all valid moves, in subjective coordinates.
        The key is the coordinates of a piece (`tuple`), and the value is a `list` of destination coordinates.'''
        moves = dict()
        for p in self.pieces[playerNum]:
            p_moves_list = self.getValidMoves(p.getCoor(), playerNum)
            if p_moves_list == []: continue
            p_subj_coor = obj_to_subj_coor(p.getCoor(), playerNum)
            moves[p_subj_coor] = [obj_to_subj_coor(i, playerNum) for i in p_moves_list]
        return moves

    def movePiece(self, start: tuple, end: tuple):
        assert self.board[start] != None and self.board[end] == None, "AssertionError at movePiece()"
        self.board[start].setCoor(end)
        self.board[end] = self.board[start]
        self.board[start] = None

    def drawBoard(self, window: pygame.Surface, playerNum: int=1):
        '''inputs Surface object'''
        self.drawPolygons(window, playerNum)
        self.drawLines(window)
        self.drawCircles(window, playerNum)

    def drawCircles(self, window:pygame.Surface, playerNum: int):
        for obj_coor in self.board:
            coor = obj_to_subj_coor(obj_coor, playerNum)
            c = add(self.centerCoor, mult(h2c(coor),self.unitLength)) #absolute coordinates on screen
            pygame.draw.circle(window, WHITE, c, self.circleRadius)
            pygame.draw.circle(window, BLACK, c, self.circleRadius, self.lineWidth)
            if isinstance(self.board[obj_coor], Piece):
                pygame.draw.circle(window, PLAYER_COLORS[self.board[obj_coor].getPlayerNum()-1], c, self.circleRadius-2)
            # coor_str = str(coor)
            # text = pygame.font.Font(size=14).render(coor_str, True, BLACK, None)
            # textRect = text.get_rect()
            # textRect.center = c
            # window.blit(text, textRect)

    def drawLines(self, window: pygame.Surface):
        '''Draws the black lines of the board. Doesn't need playerNum'''
        visited = set()
        neighbors = set()
        for coor in self.board:
            for dir in DIRECTIONS:
                n_coor = add(coor,dir)
                if n_coor not in visited and n_coor in self.board:
                    neighbors.add(n_coor)
            for n_coor in neighbors:
                c = add(self.centerCoor, mult(h2c(coor),self.unitLength))
                n = add(self.centerCoor, mult(h2c(n_coor),self.unitLength))
                pygame.draw.line(window, BLACK, c, n, self.lineWidth)
            neighbors.clear()
        # self.screen_is_altered = False

    def drawPolygons(self, window: pygame.Surface, playerNum: int=1):
        #center hexagon
        pygame.draw.polygon(window, WHITE, (abs_coors(self.centerCoor, (-4,4), self.unitLength), abs_coors(self.centerCoor, (0,4), self.unitLength), abs_coors(self.centerCoor, (4,0), self.unitLength), abs_coors(self.centerCoor, (4,-4), self.unitLength), abs_coors(self.centerCoor, (0,-4), self.unitLength), abs_coors(self.centerCoor, (-4,0), self.unitLength)))
        #triangles
        if playerNum == 1: colors = (YELLOW, RED, GREEN)
        elif playerNum == 2: colors = (RED, GREEN, YELLOW)
        elif playerNum == 3: colors = (GREEN, YELLOW, RED)
        pygame.draw.polygon(window, colors[0], (add(self.centerCoor,mult(h2c((-4,8)), self.unitLength)), add(self.centerCoor,mult(h2c((-4,4)), self.unitLength)), add(self.centerCoor,mult(h2c((0,4)), self.unitLength))))
        pygame.draw.polygon(window, colors[0], (add(self.centerCoor,mult(h2c((0,-4)), self.unitLength)), add(self.centerCoor,mult(h2c((4,-4)), self.unitLength)), add(self.centerCoor,mult(h2c((4,-8)), self.unitLength))))
        pygame.draw.polygon(window, colors[2], (add(self.centerCoor,mult(h2c((-4,0)), self.unitLength)), add(self.centerCoor,mult(h2c((-4,-4)), self.unitLength)), add(self.centerCoor,mult(h2c((0,-4)), self.unitLength))))
        pygame.draw.polygon(window, colors[2], (add(self.centerCoor,mult(h2c((0,4)), self.unitLength)), add(self.centerCoor,mult(h2c((4,4)), self.unitLength)), add(self.centerCoor,mult(h2c((4,0)), self.unitLength))))
        pygame.draw.polygon(window, colors[1], (add(self.centerCoor,mult(h2c((4,0)), self.unitLength)), add(self.centerCoor,mult(h2c((8,-4)), self.unitLength)), add(self.centerCoor,mult(h2c((4,-4)), self.unitLength))))
        pygame.draw.polygon(window, colors[1], (add(self.centerCoor,mult(h2c((-8,4)), self.unitLength)), add(self.centerCoor,mult(h2c((-4,4)), self.unitLength)), add(self.centerCoor,mult(h2c((-4,0)), self.unitLength))))

