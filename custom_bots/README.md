# Custom Bot Guide (under construction)
> [!NOTE]
> This guide is under construction.
## Coordinate System

The board of Chinese Checkers is a hexagonal board. There are three axes and six directions. However, we can define it under a two-dimensional coordinate system similar to the Cartesian, using only two parameters to describe each unique square. The third axis can be calculated from the first two.

In this project, the direction to the right is defined as the x-axis, and the direction to the top right as the y-axis. Thus, the direction to the top left is the (-x+y) axis. The spot where the axes meet is defined as `(0, 0)`.

<img src="https://github.com/henrychess/pygame-chinese-checkers/blob/main/images/coor2.png" width=500>

Here's a more concise cheat sheet for the six unit vectors:

<img src="https://github.com/henrychess/pygame-chinese-checkers/blob/main/images/coor1.png" width=250>



The coordinates and vectors are represented internally as `tuple(int, int)`. If you want to do calculations to the coordinates, use the following functions. They all return a `tuple(int, int)`. They are imported from `game_logic.helpers` (already done that in the template).

| Function | Explanation |
|----------|-------------|
|`add(tuple, tuple)`|Add up the vectors. For example, `add((1,3),(5,7))` returns `(6,10)`.|
|`mult(tuple, int)`|Multiply the vector by an integer. For example, `mult((1,2),4)` returns `(4,8)`.|

The coordinates you play with inside `pickMove()` are all "subjective" coordinates, i.e. they look the same no matter which side you are actually on. The direction to the right is always `(1,0)` to your bot, even though it may actually be something like `(0,-1)` to the game board. To return the move your bot makes, do this:
```py
# start and end are the coordinates. If you prefer other variable names, change the names below accordingly.
return [subj_to_obj_coor(start, self.playerNum), subj_to_obj_coor(end, self.playerNum)]
```

## Functions

The following three functions from `game_logic.game` grab stuff that may be helpful for your bot to choose a move.

| Function | Data Type | Explanation |
|----------|------------------|-------------|
|`allMovesDict()`|`dict(tuple(int,int):list(tuple(int,int)))`|Returns a dictionary with the coordinates of each piece as key, and the valid destination coordinates a piece can go to as value.|
|`getBoardState()`|`dict(tuple(int,int):int)`|Returns the board state in dictionary form: the key is each coordinate on the board, and the value is either 0, 1, 2, or 3: 0 means the spot is vacant, otherwise it's the occupying piece's `playerNum`.|
|`getBoolBoardState()`|`dict(tuple(int,int):bool)`|Similar to `getBoardState()`. However, it only uses `False` and `True` as value. `False` means the spot is vacant, and `True` means it is occupied.|

When you return the coordinates, remember to run the coordinates through `subj_to_obj_coor()`, like in the example in `CustomBotTemplate.py`.

## Constants

There are a few useful constants, or literals, from `game_logic.literals`.

| Constant | Data Type | Explanation |
|----------|-----------|-------------|
|`START_COOR`|`dict(int:set(tuple(int,int)))`|The key is the `playerNum` of each player (1, 2, 3). The value is a `set` of coordinates of the starting squares.|
|`END_COOR`|`dict(int:set(tuple(int,int)))`|Similar to `START_COOR`, but the value is a `set` of coordinates of the ending (destination) squares.|
|`NEUTRAL_COOR`|`set(tuple(int,int))`|A `set` of coordinates of the neutral zone.|
|`ALL_COOR`|`set(tuple(int,int))`|A `set` of all coordinates on the board.|
|`DIRECTIONS`|`set(tuple(int,int))`|A `set` of unit vectors of all six directions. Namely, `{(1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1)}`.|
