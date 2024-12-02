"""
Helper functions to determine moves in the game.
"""
import math
from game_logic.layout import DIRECTIONS


def add(a: tuple, b: tuple):
    """Insert two tuples, return them added as if they were vectors."""
    if len(a) != len(b):
        raise TypeError("tuples of different length")
    return tuple(a[i] + b[i] for i in range(len(a)))


def mult(a: tuple, n: int):
    """Insert a tuple and an int, return them multiplied as if the tuple were a vector."""
    return tuple(a[i] * n for i in range(len(a)))


def absValues(iterable):
    """Inputs an iterable with all ints. Returns a list of their absolute values."""
    return [abs[int(i)] for i in iterable]


def checkJump(
    moves: list,
    board: dict,
    destination: tuple,
    direction: tuple,
    playerNum: int,
):
    """
    Recursively checks if you can jump further. Helper function of getValidMoves().
    Inputs and outputs are in objective coordinates
    """
    for dir in DIRECTIONS:
        jumpDir = mult(dir, 2)
        if (
            dir == mult(direction, -1)
            or add(destination, dir) not in board
            or add(destination, jumpDir) not in board
            or add(destination, jumpDir) in moves
        ):
            continue
        elif board[add(destination, dir)] is None:
            continue
        else:
            dest = add(destination, jumpDir)
        if dest in moves:
            continue  # prevents endless loops
        elif dest not in board or board[dest] is not None:
            continue  # out of bounds or two pieces in a line
        else:
            moves.append(dest)
            try:
                checkJump(
                    moves,
                    board,
                    dest,
                    dir,
                    playerNum,
                )  # recursively checks available squares
            except RecursionError:
                print(
                    "RecursionError from " + str(destination) + " to " + str(dest),
                )


def setItem(list_, index, item):
    list_[index] = item


def obj_to_subj_coor(c: tuple, playerNum: int, layout: str):
    p, q, r = c[0], c[1], 0 - c[0] - c[1]
    # c: (0, -4) -> pqr: (0, -4, 4)
    # c: (1, -4) -> pqr: (1, -4, 3)
    # c: (2, -4) -> pqr: (2, -4, 2)
    # c: (3, -4) -> pqr: (3, -4, 1)
    # c: (-2, 4) -> pqr: (-2, 4, -2)
    if layout == "MIRROR":
        if playerNum == 1:
            return c
        if playerNum == 2:  # triangle player 5
            return (-p, -q)
        if playerNum == 3:  # triangle player 4
            return (-q, -r)
        if playerNum == 4:  # triangle player 3
            return (q, r)
        if playerNum == 5:  # triangle player 2
            return (r, p)
        if playerNum == 6:  # triangle player 6
            return (-r, -p)
    elif layout == "TRIANGLE":
        if playerNum == 1:
            return c
        if playerNum == 2:
            return (r, p)
        if playerNum == 3:
            return (q, r)
        if playerNum == 4:
            return (-q, -r)
        if playerNum == 5:
            return (-p, -q)
        if playerNum == 6:
            return (-r, -p)
    else:
        raise ValueError("Invalid layout")


def subj_to_obj_coor(c: tuple, playerNum: int, layout: str):
    p, q, r = c[0], c[1], 0 - c[0] - c[1]
    # c: (0, -4) -> pqr: (0, -4, 4)
    # c: (1, -4) -> pqr: (1, -4, 3)
    # c: (2, -4) -> pqr: (2, -4, 2)
    # c: (3, -4) -> pqr: (3, -4, 1)
    # c: (-2, 4) -> pqr: (-2, 4, -2)
    # c: (-3, -1) -> pqr: (-3, -1, 4)
    if layout == "MIRROR":
        if playerNum == 1:
            return c
        if playerNum == 2:  # triangle player 5
            return (-p, -q)
        if playerNum == 3:  # triangle player 4
            return (-r, -p)
        if playerNum == 4:  # triangle player 3
            return (r, p)
        if playerNum == 5:  # triangle player 2
            return (q, r)
        if playerNum == 6:  # triangle player 6
            return (-q, -r)
    elif layout == "TRIANGLE":
        if playerNum == 1:
            return c
        if playerNum == 2:
            return (q, r)
        if playerNum == 3:
            return (r, p)
        if playerNum == 4:
            return (-r, -p)
        if playerNum == 5:
            return (-p, -q)
        if playerNum == 6:
            return (-q, -r)
    else:
        raise ValueError("Invalid layout")


def sign_func(i: int):
    if i > 0:
        return 1
    if i < 0:
        return -1
    else:
        return 0


def distance(start: tuple, end: tuple):
    i = 0
    c = start
    p2 = end[0]
    q2 = end[1]
    while c != end:
        p1 = c[0]
        q1 = c[1]
        dp = sign_func(p2 - p1)
        dq = sign_func(q2 - q1)
        if (dp == 1 and dq == 1) or (dp == -1 and dq == -1):
            dq = 0
        c = add(c, (dp, dq))
        i += 1
    return i


def rotate(coor: tuple, angleDegrees):
    x = coor[0]
    y = coor[1]
    angle = math.radians(angleDegrees)
    return (
        math.cos(angle) * x - math.sin(angle) * y,
        math.sin(angle) * x + math.cos(angle) * y,
    )


def h2c(coor: tuple):
    """hexagonal to cartesian for pygame"""
    x = coor[0]
    y = coor[1]
    x2 = x + 0.5 * y
    y2 = -1 * 0.5 * (math.sqrt(3) * y)
    return (x2, y2)


def abs_coors(center: tuple, coor: tuple, unit: int):
    """absolute coordinates on screen"""
    return add(center, mult(h2c(coor), unit))


def ints(s):
    l = [int(i) for i in s]
    if isinstance(s, tuple):
        return tuple(l)
    if isinstance(s, list):
        return l
    if isinstance(s, set):
        return set(l)
