"""
Game Class to represent the game state and logic.
"""
import copy
from game_logic.helpers import add, checkJump, obj_to_subj_coor, mult
from game_logic.layout import (
    DIRECTIONS,
    ALL_COOR,
    Layout,
)
from game_logic.piece import Piece
from gui.constants import HEIGHT, WIDTH
from typing import List


class Move:
    """
    Class to backtrace the path of a move.
    """

    def __init__(self, coord: tuple):
        self.parent: Move = None
        self.coord: tuple = coord
        self.children: List[Move] = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def getPath(self) -> List[tuple]:
        """
        Recursively add the parent to the path.
        """
        path = [self.coord]
        if self.parent is self:  # reached the root node
            return path
        else:  # recurse
            return self.parent.getPath() + path


class Game:
    def __init__(
        self,
        playerList,
        playerNum: int,
        playerNames: list[str],
        layout: str,
        n_pieces: int,
    ):
        # Gameplay variables
        self.turnCount = 1  # current turn number
        self.playerNum = playerNum  # current player number (1->6)
        self.playerNames = playerNames  # e.g. ["Human", "GreedyBot1"]
        # e.g. ["Human", "GreedyBot1"], used in gui_helpers.drawTurnCount()
        self.playerList = playerList  # list of player objects
        # e.g. [<game_logic.human.Human object at 0x000001F1E4428DA0>,
        #       <bots.GreedyBot1.GreedyBot1 object at 0x000001F1E5AEA660>]

        # Instantiate pieces and board
        self.pieces: dict[int, set[Piece]] = {}
        self.board: dict[tuple, Piece | None] = {}
        self.layout = layout
        self.coor = Layout(layout, n_pieces)
        self.createBoard()

        # Parameters for drawing board
        self.unitLength = int(WIDTH * 0.05)  # unitLength length in pixels
        self.lineWidth = int(self.unitLength * 0.05)
        self.circleRadius = int(HEIGHT * 0.025)  # board square (circle) radius
        self.centerCoor = (WIDTH / 2, HEIGHT / 2)

    def createBoard(self):
        """
        Returns a dict of the board. Adds pieces to starting zones.
        """
        playerCount = len(self.playerList)

        for i in range(1, playerCount + 1):
            self.pieces[i] = set()

        # Initialize all possible positions
        for x, y in ALL_COOR:
            self.board[(x, y)] = None
        # Add empty spaces first because a player's start zones overlaps with
        # another player's end zone

        # Add pieces
        for playerNum in range(1, playerCount + 1):
            for p, q in self.coor.START_COOR[playerNum]:
                # Add piece to board
                self.board[(p, q)] = Piece(playerNum, p, q)
                # Add piece to player's set
                self.pieces[playerNum].add(self.board[p, q])

    def getValidMoves(self, startPos: tuple, playerNum: int):
        """
        Compute all valid moves for a piece.

        Args:
            startPos (tuple): objective coordinates of the piece.
            playerNum (int): the player number.

        Returns:
            list of tuples: objective coordinates of the dest valid moves.
        """
        moves = []

        # Try all 6 directions
        for direction in DIRECTIONS:
            destination = add(startPos, direction)
            # Step is out of bounds
            if destination not in self.board:
                continue

            # Single step into open space
            if self.board[destination] is None:
                moves.append(destination)  # walk

            # Single step into occupied space, check for skips
            else:  # self.board[destination] is not None
                destination = add(destination, direction)
                if destination not in self.board or self.board[destination] is not None:
                    continue  # out of bounds or can't jump
                moves.append(destination)
                checkJump(moves, self.board, destination, direction, playerNum)

        # You can move past other player's territory, but you can't stay there.
        for i in copy.deepcopy(moves):
            if (
                (i not in self.coor.START_COOR[playerNum])
                and (i not in self.coor.END_COOR[playerNum])
                and (i not in self.coor.NEUTRAL_COOR)
            ):
                while i in moves:
                    moves.remove(i)
        return list(set(moves))

    def checkValidStepDest(self, playerNum: int, dest: tuple):
        """
        Check if the destination is valid single step for the player.

        Args:
            playerNum (int): the player number.
            dest (tuple): the objective coordinates of the destination.

        Returns:
            bool: True if the destination is valid.
        """
        if dest not in self.board:  # out of bounds
            # print("out of bounds")
            return False
        if self.board[dest] is not None:  # occupied cell
            # print("occupied cell")
            return False
        if (
            dest in self.coor.NEUTRAL_COOR  # neutral territory
            or dest in self.coor.START_COOR[playerNum]  # own start zone
            or dest in self.coor.END_COOR[playerNum]
        ):  # own end zone
            return True
        return False
        # if (
        #     dest not in NEUTRAL_COOR  # other player's territory
        #     and dest not in END_COOR[playerNum]
        #     and dest not in START_COOR[playerNum]
        # ):
        #     # print("other player's territory")
        #     return False
        # return True

    def getMovePath(self, playerNum: int, start: tuple, end: tuple):
        """
        Find the path for the move using breadth-first search.

        Note:
            This function should be called before moving the piece,
            otherwise the end cell will be occupied.

        Args:
            playerNum (int): the player number.
            start (tuple): objective coordinates of the starting cell.
            end (tuple): objective coordinates of the ending cell.

        Returns:
            path (list(tuples)): objective coordinates of cells along the path.
        """
        start_m = Move(start)
        start_m.parent = start_m
        path = []

        # Single step
        for dir in DIRECTIONS:
            dest = add(start, dir)
            dest_m = Move(dest)
            if not self.checkValidStepDest(playerNum, dest):
                continue
            start_m.addChild(dest_m)
            # Found end cell, return path
            if dest == end:
                path += dest_m.getPath()
                return path

        # Jump steps using BFS. Note that a jump can be made through
        # opponent's territory.
        queue = [start_m]
        while queue:
            current = queue.pop(0)
            for dir in DIRECTIONS:
                # print(f"dir: {dir}")
                stepDest = add(current.coord, dir)
                if stepDest not in self.board:  # out of bounds
                    # print("step: out of bounds")
                    continue
                if self.board[stepDest] is None:  # no piece to skip
                    # print("step: no piece to skip")
                    continue
                jumpDir = mult(dir, 2)
                jumpDest = add(current.coord, jumpDir)
                jumpDest_m = Move(jumpDest)  # create Move object
                if jumpDest not in self.board:  # out of bounds
                    # print("jump: out of bounds")
                    continue
                if self.board[jumpDest] is not None:  # occupied cell
                    # print("jump: occupied cell", jumpDest)
                    continue
                if jumpDest == current.parent.coord:
                    # print("jump: back to parent")
                    continue  # prevents endless loops

                jumpDest_m.parent = current
                current.addChild(jumpDest_m)
                if jumpDest == end:
                    path += jumpDest_m.getPath()
                    return path
                queue.append(jumpDest_m)

        # Assumes that a path will be found eventually.
        if path == []:
            raise ValueError("No path found")

    def checkWin(self, playerNum: int):
        """
        Check if all of the player's pieces are in their end zone.
        """
        for i in self.coor.END_COOR[playerNum]:
            # if there are no pieces
            if self.board[i] is None:
                return False
            # if the piece does not belong to the player
            if (
                isinstance(self.board[i], Piece)
                and self.board[i].getPlayerNum() != playerNum
            ):
                return False
        return True

    def isOver(self):
        """
        Check if the game is over.
        """
        for i in range(1, len(self.playerList) + 1):
            if self.checkWin(i):
                return True
        return False

    def getBoardState(self, playerNum: int):
        """
        Key: subjective coordinates
        Value: piece's player number,
        or 0 if it's vacant
        """
        state = dict()
        for i in self.board:
            state[obj_to_subj_coor(i, playerNum, self.layout)] = (
                0 if self.board[i] is None else int(self.board[i].getPlayerNum())
            )
        return state

    def getBoolBoardState(self, playerNum: int):
        """
        Returns a dict of the board in subjective coordinates.

        Key: subjective coordinates
        Value: true if occupied, false if vacant
        """
        state = dict()
        for i in self.board:
            state[obj_to_subj_coor(i, playerNum, self.layout)] = (
                self.board[i] is not None
            )
        return state

    def allMovesDict(self, playerNum: int):
        """
        Returns a dict of all valid moves, in subjective coordinates.

        Key: coordinates of a piece (`tuple`),
        Value: list of destination coordinates.

        e.g. {(1, -5): [(1, -4), (0, -4)], (3, -5): [(4, -6), (2, -4)]}
        """
        moves = dict()
        for p in self.pieces[playerNum]:
            p_moves_list = self.getValidMoves(p.getCoor(), playerNum)
            if p_moves_list == []:
                continue
            p_subj_coor = obj_to_subj_coor(p.getCoor(), playerNum, self.layout)
            moves[p_subj_coor] = [
                obj_to_subj_coor(i, playerNum, self.layout) for i in p_moves_list
            ]
        # print(f"[Game] All moves (sub): {moves}")
        return moves

    def movePiece(self, start: tuple, end: tuple):
        """
        Moves a piece from start coord to end coord. in objective coordinates.
        """
        assert self.board[start] is not None, "startCoord is empty"
        assert self.board[end] is None, "endCoord is occupied"

        # Update piece attribute
        self.board[start].setCoor(end)

        # Change piece's location in g.board
        self.board[end] = self.board[start]
        self.board[start] = None
