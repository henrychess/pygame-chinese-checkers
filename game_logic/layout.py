"""
This file contains literals used in the game logic.

The following literals are defined:
- START_COOR: dict
- END_COOR: dict
- NEUTRAL_COOR: set
- ALL_COOR: set
- DIRECTIONS: set
- POINTS: set
"""

# Unit vectors for the 6 directions from a cell
DIRECTIONS = {(1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1)}

# Zones start clockwise from the bottom-most middle yellow triangle.
# 10 piece configuration
ZONE_1_10 = {
    (4, -8),
    (3, -7),
    (4, -7),
    (2, -6),
    (3, -6),
    (4, -6),
    (1, -5),
    (2, -5),
    (3, -5),
    (4, -5),
}
ZONE_2_10 = {
    (-4, -2),
    (-4, -1),
    (-3, -2),
    (-4, -3),
    (-3, -3),
    (-2, -3),
    (-1, -4),
    (-4, -4),
    (-3, -4),
    (-2, -4),
}
ZONE_3_10 = {
    (-5, 1),
    (-5, 4),
    (-7, 4),
    (-6, 4),
    (-5, 3),
    (-5, 2),
    (-7, 3),
    (-6, 3),
    (-8, 4),
    (-6, 2),
}
ZONE_4_10 = {
    (-4, 7),
    (-3, 7),
    (-1, 5),
    (-4, 6),
    (-3, 6),
    (-2, 6),
    (-4, 5),
    (-3, 5),
    (-4, 8),
    (-2, 5),
}
ZONE_5_10 = {
    (4, 4),
    (2, 4),
    (3, 4),
    (4, 1),
    (4, 3),
    (1, 4),
    (4, 2),
    (2, 3),
    (3, 3),
    (3, 2),
}
ZONE_6_10 = {
    (6, -4),
    (7, -3),
    (5, -2),
    (5, -1),
    (6, -2),
    (5, -3),
    (6, -3),
    (7, -4),
    (8, -4),
    (5, -4),
}

# Zones start clockwise from the bottom-most middle yellow triangle.
# 15 piece configuration
ZONE_1_15 = {
    (4, -8),
    (3, -7),
    (4, -7),
    (2, -6),
    (3, -6),
    (4, -6),
    (1, -5),
    (2, -5),
    (3, -5),
    (4, -5),
    (0, -4),
    (1, -4),
    (2, -4),
    (3, -4),
    (4, -4),
}
ZONE_2_15 = {
    (-4, -2),
    (-4, -1),
    (-3, -2),
    (-3, -1),
    (-2, -2),
    (-4, -3),
    (-3, -3),
    (-4, 0),
    (-2, -3),
    (-1, -3),
    (0, -4),
    (-1, -4),
    (-4, -4),
    (-3, -4),
    (-2, -4),
}
ZONE_3_15 = {
    (-4, 4),
    (-5, 1),
    (-4, 1),
    (-5, 4),
    (-7, 4),
    (-6, 4),
    (-4, 0),
    (-5, 3),
    (-4, 3),
    (-5, 2),
    (-7, 3),
    (-4, 2),
    (-6, 3),
    (-8, 4),
    (-6, 2),
}
ZONE_4_15 = {
    (-4, 4),
    (-3, 4),
    (0, 4),
    (-4, 7),
    (-2, 4),
    (-3, 7),
    (-1, 4),
    (-1, 5),
    (-4, 6),
    (-3, 6),
    (-2, 6),
    (-4, 5),
    (-3, 5),
    (-4, 8),
    (-2, 5),
}
ZONE_5_15 = {
    (4, 4),
    (2, 4),
    (4, 0),
    (0, 4),
    (3, 4),
    (4, 1),
    (3, 1),
    (4, 3),
    (1, 4),
    (4, 2),
    (2, 3),
    (3, 3),
    (2, 2),
    (3, 2),
    (1, 3),
}
ZONE_6_15 = {
    (6, -4),
    (4, 0),
    (4, -3),
    (7, -3),
    (5, -2),
    (5, -1),
    (6, -2),
    (4, -4),
    (5, -3),
    (6, -3),
    (7, -4),
    (8, -4),
    (4, -1),
    (4, -2),
    (5, -4),
}

# Set of neutral coordinates in the center of the board
NEUTRAL_ZONE = {
    (3, -2),
    (3, -1),
    (-3, 0),
    (-3, 3),
    (0, 2),
    (1, -3),
    (1, 0),
    (-2, -1),
    (-1, -2),
    (-1, -1),
    (-2, 1),
    (-1, 1),
    (3, -3),
    (3, 0),
    (-3, 2),
    (0, -1),
    (0, -2),
    (0, 1),
    (2, -2),
    (2, -1),
    (1, 2),
    (2, 1),
    (-2, 0),
    (-1, 0),
    (-2, 3),
    (-1, 3),
    (-2, 2),
    (0, -3),
    (-3, 1),
    (0, 0),
    (2, -3),
    (1, 1),
    (0, 3),
    (2, 0),
    (1, -2),
    (1, -1),
    (-1, 2),
}

# Outer ring of neutral zone in the center
NEUTRAL_RING = {
    (0, -4),
    (1, -4),
    (2, -4),
    (3, -4),
    (4, -4),
    (4, -3),
    (4, -2),
    (4, -1),
    (4, 0),
    (3, 1),
    (2, 2),
    (1, 3),
    (0, 4),
    (-1, 4),
    (-2, 4),
    (-3, 4),
    (-4, 4),
    (-4, 3),
    (-4, 2),
    (-4, 1),
    (-4, 0),
    (-3, -1),
    (-2, -2),
    (-1, -3),
}

# All possible coordinates on the board
ALL_COOR = (
    ZONE_1_10
    | ZONE_2_10
    | ZONE_3_10
    | ZONE_4_10
    | ZONE_5_10
    | ZONE_6_10
    | NEUTRAL_ZONE
    | NEUTRAL_RING
)


class Layout:
    def __init__(self, layout: str, n_pieces: int):
        self.layout = layout  # "MIRROR" or "TRIANGLE"
        self.n_pieces = n_pieces  # 10 or 15

        self.START_COOR = {}
        self.END_COOR = {}
        self.NEUTRAL_COOR = set()

        self.set_layout()

    def set_layout(self):
        if self.n_pieces == 10:
            self.NEUTRAL_COOR = NEUTRAL_ZONE | NEUTRAL_RING
            if self.layout == "MIRROR":
                # Key: playerNum, Value: set of start coordinates
                self.START_COOR = {
                    1: ZONE_1_10,
                    2: ZONE_4_10,
                    3: ZONE_2_10,
                    4: ZONE_5_10,
                    5: ZONE_3_10,
                    6: ZONE_6_10,
                }
                self.END_COOR = {
                    1: ZONE_4_10,
                    2: ZONE_1_10,
                    3: ZONE_5_10,
                    4: ZONE_2_10,
                    5: ZONE_6_10,
                    6: ZONE_3_10,
                }

            elif self.layout == "TRIANGLE":
                self.START_COOR = {
                    1: ZONE_1_10,
                    2: ZONE_3_10,
                    3: ZONE_5_10,
                    4: ZONE_2_10,
                    5: ZONE_4_10,
                    6: ZONE_6_10,
                }
                self.END_COOR = {
                    1: ZONE_4_10,
                    2: ZONE_6_10,
                    3: ZONE_2_10,
                    4: ZONE_5_10,
                    5: ZONE_1_10,
                    6: ZONE_3_10,
                }
            else:
                raise ValueError(f"Invalid layout: {self.layout}")

        elif self.n_pieces == 15:
            self.NEUTRAL_COOR = NEUTRAL_ZONE
            if self.layout == "MIRROR":
                self.START_COOR = {
                    1: ZONE_1_15,
                    2: ZONE_4_15,
                    3: ZONE_2_15,
                    4: ZONE_5_15,
                    5: ZONE_3_15,
                    6: ZONE_6_15,
                }
                self.END_COOR = {
                    1: ZONE_4_15,
                    2: ZONE_1_15,
                    3: ZONE_5_15,
                    4: ZONE_2_15,
                    5: ZONE_6_15,
                    6: ZONE_3_15,
                }

            elif self.layout == "TRIANGLE":
                self.START_COOR = {
                    1: ZONE_1_15,
                    2: ZONE_3_15,
                    3: ZONE_5_15,
                    4: ZONE_2_15,
                    5: ZONE_4_15,
                    6: ZONE_6_15,
                }
                self.END_COOR = {
                    1: ZONE_4_15,
                    2: ZONE_6_15,
                    3: ZONE_2_15,
                    4: ZONE_5_15,
                    5: ZONE_1_15,
                    6: ZONE_3_15,
                }
            else:
                raise ValueError(f"Invalid layout: {self.layout}")
        else:
            raise ValueError(f"Invalid number of pieces: {self.n_pieces}")
