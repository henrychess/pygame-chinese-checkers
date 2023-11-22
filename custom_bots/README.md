# Custom Bot Guide (under construction)
> [!NOTE]
> This guide is under construction.
## Coordinate System

## Functions

The following three functions from `game_logic.game` grab stuff that may be helpful for your bot to choose a move.

| Function | Return Data Type | Explanation |
|----------|------------------|-------------|
|`allMovesDict()`|`dict`|Returns a dictionary with the coordinates of each piece as key, and the valid destination coordinates a piece can go to as value.|
|`getBoardState()`|`dict`|Returns the board state in dictionary form: the key is each coordinate on the board, and the value is either 0, 1, 2, or 3: 0 means the spot is vacant, otherwise it's the occupying piece's `playerNum`.|
|`getBoolBoardState()`|`dict`|Similar to `getBoardState()`. However, it only uses `False` and `True` as value. `False` means the spot is vacant, and `True` means it is occupied.|

When you return the coordinates, remember to 
run the coordinates through `subj_to_obj_coor()`, 
like in the example in `CustomBotTemplate.py`.

## Constants
