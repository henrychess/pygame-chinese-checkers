"""
Class to represent a piece on the board. Each piece has a player number,
and a position on the board.
"""


class Piece:
    def __init__(self, playerNum: int, p: int, q: int):
        self.playerNum = playerNum
        self.p = p
        self.q = q
        self.mouse_hovering = False
        self.selected = False

    def __hash__(self) -> int:
        return id(self)

    def getPlayerNum(self):
        return self.playerNum

    def getCoor(self):
        return (self.p, self.q)

    def setCoor(self, new_coor: tuple):
        self.p = new_coor[0]
        self.q = new_coor[1]
