from game_logic.player import Player
from game_logic.game import *

class CustomBotTemplate(Player):
    def __init__(self):
        super().__init__()
    
    def pickMove(self, g:Game):
        """
            The following three functions grab stuff
        that may be helpful for your bot to choose
        a move.
            Remember, all the functions return in
        *subjective* coordinates. It doesn't matter
        if you go first, second, or third.
            The first one, allMovesDict, returns a
        dictionary with the coordinates of each piece
        as key, and the valid destination coordinates
        a piece can go to as value.
            The second one, getBoardState, returns the 
        board state in dictionary form: the key is each
        coordinate on the board, and the value is either
        0, 1, 2, or 3: 0 means the spot is vacant,
        otherwise it's the occupying piece's playerNum.
            The third one, getBoolBoardState, is similar
        to the second one. However, it only uses False
        and True as value. False means the spot is vacant,
        while True means it is occupied.
            When you return the coordinates, remember to 
        run the coordinates through subj_to_obj_coor(), 
        like in the example below.
        """
        moves = g.allMovesDict(self.playerNum)
        #board_state = g.getBoardState(self.playerNum)
        #bool_board_state = g.getBoolBoardState(self.playerNum)
        """
        The following code section is a simple example: it
        randomly picks a valid move and return it.
        """
        from random import choice
        l = []
        for coor in moves:
            if moves[coor] != []: l.append(coor)
        start = choice(l)
        end = choice(moves[start])
        """
        This is the return section. `start` and `end` are
        the starting and ending subjective coordinates.
        """
        return [subj_to_obj_coor(start, self.playerNum),
                subj_to_obj_coor(end, self.playerNum)]
