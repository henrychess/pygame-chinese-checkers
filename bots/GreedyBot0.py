import random
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor
from game_logic.player import Player


class GreedyBot0(Player):
    """
    Choose a forward move randomly. Else, choose a sideway move randomly.
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Choose a forward move randomly. Else, choose a sideway move randomly.

        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"[GreedyBot0] is player {self.playerNum}")
        moves = g.allMovesDict(self.playerNum)
        forwardMoves = dict()
        sidewaysMoves = dict()
        (start_coor, end_coor) = ((), ())

        # Split moves into forward and sideways
        for coor in moves:
            # If there are moves
            if moves[coor] != []:
                forwardMoves[coor] = []
                sidewaysMoves[coor] = []

            # Check y-coordinate of destination
            for dest in moves[coor]:
                if dest[1] > coor[1]:
                    forwardMoves[coor].append(dest)
                if dest[1] == coor[1]:
                    sidewaysMoves[coor].append(dest)

        # Remove empty keys
        for coor in list(forwardMoves):
            if forwardMoves[coor] == []:
                del forwardMoves[coor]
        for coor in list(sidewaysMoves):
            if sidewaysMoves[coor] == []:
                del sidewaysMoves[coor]

        # Choose a forward move randomly
        if len(forwardMoves) != 0:
            start_coor = random.choice(list(forwardMoves))
            end_coor = random.choice(forwardMoves[start_coor])
        # Else, choose a sideway move randomly
        else:
            start_coor = random.choice(list(sidewaysMoves))
            end_coor = random.choice(sidewaysMoves[start_coor])

        move = [
            subj_to_obj_coor(start_coor, self.playerNum, g.layout),
            subj_to_obj_coor(end_coor, self.playerNum, g.layout),
        ]
        print(f"[GreedyBot0] Move: {move}\n")
        return move
