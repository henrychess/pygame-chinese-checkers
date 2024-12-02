import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class GreedyBot1(Player):
    """
    Choose the move that moves a piece to the topmost cell.
    """

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Choose the forward move with the greatest y value. If there are no
        forward moves, choose a sideway move randomly.

        Returns:
            [startCoor, endCoor] : in objective coordinates
        """
        print(f"[GreedyBot1] is player {self.playerNum}")
        moves = g.allMovesDict(self.playerNum)
        forwardMoves = dict()
        sidewaysMoves = dict()
        (startCoor, endCoor) = ((), ())

        # Split moves into forward and sideways
        for startCoor in moves:
            # Check y-coordinate of destination
            for dest in moves[startCoor]:
                if dest[1] > startCoor[1]:
                    forwardMoves[startCoor] = dest
                if dest[1] == startCoor[1]:
                    sidewaysMoves[startCoor] = dest
        # BUG: moves return int when there are no forward moves

        # If there are no forward moves, move sideways randomly.
        if len(forwardMoves) == 0:
            print("[GreedyBot1] No forward moves")
            print(sidewaysMoves)
            startCoor = random.choice(list(sidewaysMoves))
            endCoor = random.choice(sidewaysMoves[startCoor])

            move = [
                subj_to_obj_coor(startCoor, self.playerNum, g.layout),
                subj_to_obj_coor(endCoor, self.playerNum, g.layout),
            ]
            print(f"[GreedyBot1] Move: {move}\n")
            return move

        # Choose the furthest destination (biggest y value in dest),
        # then backmost piece (smallest y value in coor)
        biggestDestY = -8
        smallestStartY = 8
        for coor in forwardMoves:
            dest = forwardMoves[coor]
            # Find forward move with biggest y dest value
            if dest[1] > biggestDestY:
                (startCoor, endCoor) = (coor, dest)
                biggestDestY = dest[1]
                smallestStartY = coor[1]

            elif dest[1] == biggestDestY:
                startY = coor[1]

                # If tiebreakers,
                # choose forward move with smallest y start value
                if startY < smallestStartY:
                    (startCoor, endCoor) = (coor, dest)
                    biggestDestY = dest[1]
                    smallestStartY = coor[1]
                elif startY == smallestStartY:
                    startCoor, endCoor = random.choice(
                        [[startCoor, endCoor], [coor, dest]],
                    )
                    biggestDestY = endCoor[1]
                    smallestStartY = startCoor[1]

        move = [
            subj_to_obj_coor(startCoor, self.playerNum, g.layout),
            subj_to_obj_coor(endCoor, self.playerNum, g.layout),
        ]
        print(f"[GreedyBot1] Move: {move}\n")
        return move
