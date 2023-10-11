#literals
DIRECTIONS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)) #six ways of movement
END_COORDINATES = {1:[(-4, 4),(-4, 5),(-4, 6),(-4, 7),(-4, 8),(-3, 4),(-3, 5),(-3, 6),(-3, 7),(-2, 4),(-2, 5),(-2, 6),(-1, 4),(-1, 5),(0, 4)],
2:[(4, -4),(4, -3),(4, -2),(4, -1),(4, 0),(5, -4),(5, -3),(5, -2),(5, -1),(6, -4),(6, -3),(6, -2),(7, -4),(7, -3),(8, -4)],
3:[(0, -4),(-4, 0),(-4, -4),(-4, -3),(-4, -2),(-4, -1),(-3, -4),(-3, -3),(-3, -2),(-3, -1),(-2, -4),(-2, -3),(-2, -2),(-1, -4),(-1, -3)]}

def gameBoard():
    '''
    Returns a dictionary representing an empty Chinese Checkers board.
    The key is a tuple and represents the coordinates of a square.
    The value is a list of two elements:
    The first is a list representing whose land the square belongs to. The negative sign means it's an end zone.
    The second is the player's number the occupied piece belongs to. It's 0 if the square is unoccupied.
    '''
    #initializing the board
    Board = {}
    #player 1 end zone
    for p in range(-4,1):
        for q in range(4,9):
            if p + q > 4:
                continue
            else:
                Board[(p,q)] = [[-1],0]
    #player 1 start zone
    for p in range(0,5):
        for q in range(-8,-3):
            if p + q < -4:
                continue
            else:
                Board[(p,q)] = [[1],0]
    #player 2 end zone
    for p in range(4,9):
        for q in range(-4,1):
            if p + q > 4:
                continue
            else:
                if (p,q) in Board:
                    Board[(p,q)][0].append(-2)
                else:
                    Board[(p,q)] = [[-2],0]
    #player 2 start zone
    for p in range(-8,-3):
        for q in range(0,5):
            if p + q < -4:
                continue
            else:
                if (p,q) in Board:
                    Board[(p,q)][0].append(2)
                else:
                    Board[(p,q)] = [[2],0]
    #player 3 end zone
    for p in range(-4,1):
        for q in range(-4,1):
            if p + q > -4:
                continue
            else:
                if (p,q) in Board:
                    Board[(p,q)][0].append(-3)
                else:
                    Board[(p,q)] = [[-3],0]
    #player 3 start zone
    for p in range(0,5):
        for q in range(0,5):
            if p + q < 4:
                continue
            else:
                if (p,q) in Board:
                    Board[(p,q)][0].append(3)
                else:
                    Board[(p,q)] = [[3],0]
    #neutral zone
    for p in range(-3,4):
        for q in range(-3,4):
            if p + q <= 3 and p + q >= -3:
                Board[(p,q)] = [[0],0]
    return Board

def getDestination(startPos, direction):
    '''Inputs starting position and direction vector (iterables). Returns destination coordinates in tuple.'''
    assert len(startPos) == len(direction)
    tempList = list(startPos)
    for i in range(len(startPos)):
        tempList[i] += direction[i]
    return tuple(tempList)

def checkJump(moves: set, board: dict, destination: tuple, direction: tuple):
    '''Recursively checks if you can jump further. Helper function of getPossibleMoves().'''
    for dir in DIRECTIONS:
        if dir == oppositeDirection(direction): continue #prevents redundancy
        dest = getDestination(destination, dir)
        if dest not in board or board[dest][1] == 0: continue #out of bounds or empty neighboring square
        dest = getDestination(dest, dir)
        if dest in moves: continue #prevents endless loops
        if dest not in board or board[dest][1] != 0: continue #out of bounds or two pieces in a line
        moves.add(dest)
        checkJump(moves, board, dest, dir) #recursively checks available squares

def absValues(iterable):
    """Inputs an iterable with all ints. Returns a list of their absolute values."""
    return [abs[i] for i in iterable]

def oppositeDirection(dir: tuple):
    return tuple((-1 * ele) for ele in dir)

def getPossibleMoves(startPos: tuple, playerNum: int, board: dict):
    '''Inputs a starting position, playing player's number, and current board state.
    Returns a set of possible moves that piece can make.'''
    moves = set()
    for direction in DIRECTIONS:
        destination = getDestination(startPos, direction)
        if destination not in board: continue #out of bounds
        if board[destination][1] == 0: moves.add(destination) #walk
        else: #board[destination][1] != 0
            destination = getDestination(destination, direction)
            if destination not in board or board[destination][1] != 0: continue #out of bounds or can't jump
            moves.add(destination)
            checkJump(moves, board, destination, direction)
    for i in moves:
        #You can move past other player's territory, but you can't stay there.
        if playerNum not in absValues(board[i][0]): moves.remove(i)
    return moves

def checkWin(playerNum: int, board: dict):
    winsGame = True
    for i in END_COORDINATES[playerNum]:
        winsGame = (board[i][1] == playerNum)
        if winsGame == False: return bool(winsGame)
    return bool(winsGame)

class Board:
    def __init__(self):
        self.structure = gameBoard()
    def getBoard(self):
        return self.structure
    #def getBoardState(self):
        #boardState = {}
        #for i in self.structure:
            #boardState[i] = self.structure[i][1]
        #return boardState

class Player:
    def __init__(self, playerNum):
        self.playerNum = playerNum
    def chooseMove(self, b: Board):
        '''dummy function that should be overridden,
        passes the move to the board'''
        #board = b.getBoard()
        pass