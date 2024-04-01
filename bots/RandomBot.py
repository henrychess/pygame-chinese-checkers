import random
from game_logic.player import Player
from game_logic.game import Game
from game_logic.helpers import subj_to_obj_coor


class RandomBot(Player):
    def __init__(self):
        super().__init__()

    def pickMove(self, g: Game):
        """
        Returns:
            [start_coor, end_coor] : in objective coordinates
        """
        print(f"[RandomBot] is player {self.playerNum}")
        moves = g.allMovesDict(self.playerNum)

        start_coords = []
        for coor in moves:
            if moves[coor] != []:
                start_coords.append(coor)

        # Choose a random start_coor
        start_coor = random.choice(start_coords)
        end_coor = random.choice(moves[start_coor])

        move = [
            subj_to_obj_coor(start_coor, self.playerNum, g.layout),
            subj_to_obj_coor(end_coor, self.playerNum, g.layout),
        ]
        print(f"[RandomBot] Move: {move}\n")
        return move
