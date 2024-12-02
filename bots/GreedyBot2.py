import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class GreedyBot2(Player):
    """Always finds a move that jumps through the maximum distance (dest[1] - coor[1])"""

    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Choose a forward move with the greatest distance travelled. If there
        are no forward moves, choose a sideway move randomly.

        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"[GreedyBot2] is player {self.playerNum}")

        forwardMoves = dict()
        sidewaysMoves = dict()
        (start_coor, end_coor) = (None, None)

        # Split moves into forward and sideways
        moves = g.allMovesDict(self.playerNum)
        for coor in moves:
            if moves == []:
                continue
            forwardMoves[coor] = []
            sidewaysMoves[coor] = []
            for dest in moves[coor]:
                if dest[1] > coor[1]:
                    forwardMoves[coor].append(dest)
                if dest[1] == coor[1]:
                    sidewaysMoves[coor].append(dest)

        # If forward is empty, move sideways
        if len(forwardMoves) == 0:
            start_coor = random.choice(list(sidewaysMoves))
            end_coor = random.choice(sidewaysMoves[start_coor])
            move = [
                subj_to_obj_coor(start_coor, self.playerNum, g.layout),
                subj_to_obj_coor(end_coor, self.playerNum, g.layout),
            ]
            print(f"[GreedyBot2] Move: {move}\n")
            return move

        # Find forward with the max distance travelled
        max_dist = 0
        for coor in forwardMoves:
            for dest in forwardMoves[coor]:
                dist = dest[1] - coor[1]
                if dist > max_dist:
                    max_dist = dist
                    (start_coor, end_coor) = (coor, dest)
                elif dist == max_dist:
                    # Prefer to move the piece that is more backwards
                    if dest[1] < end_coor[1]:
                        max_dist = dist
                        (start_coor, end_coor) = (coor, dest)

        if start_coor is None or end_coor is None:
            print("[GreedyBot2] Error: No move found")
            start_coor = random.choice(list(moves))
            end_coor = random.choice(moves[start_coor])

        move = [
            subj_to_obj_coor(start_coor, self.playerNum, g.layout),
            subj_to_obj_coor(end_coor, self.playerNum, g.layout),
        ]
        print(f"[GreedyBot2] Move: {move}\n")
        return move
