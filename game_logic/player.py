"""
Abstract class for human players and bots in the game.
"""
from abc import ABC, ABCMeta, abstractmethod
from game_logic.game import Game


class PlayerMeta(ABCMeta):
    playerTypes = []

    def __init__(cls, name, bases, attrs):
        if ABC not in bases:
            PlayerMeta.playerTypes.append(cls)
        super().__init__(name, bases, attrs)


class Player(ABC, metaclass=PlayerMeta):
    def __init__(self):
        self.playerNum = 0  # Starting from 1
        self.has_won = False

    def getPlayerNum(self):
        return self.playerNum

    def setPlayerNum(self, num: int):
        """
        Starting from 1.
        """
        self.playerNum = num

    @abstractmethod
    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        ...
