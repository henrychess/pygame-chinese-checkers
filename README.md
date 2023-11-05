# pygame-chinese-checkers

> [!NOTE]
> This is a hobby project by a beginner/amateur in programming. You may encounter bugs.

## Requirements
- Python 3.8+
- `pygame-ce` and `PySide6`
To install Python itself, head to the [official website](https://www.python.org/) and follow their instructions.
You may also check your Python version by pasting this in your terminal:
```
python3 --version
```
To install `pygame-ce` and `PySide6`, paste this into your terminal (after you're sure you have Python 3.8+):
```
python3 -m pip install -U pygame-ce PySide6
```

## Running the program
To run it, first open a terminal at the folder where this project is saved at, then use:
```
python3 main.py
```
to start the game. If nothing goes wrong, the game should prompt you to select players after clicking Play.

If you want to close the window, you have to manually quit the game by clicking the X button on the top right corner (or top left, depending on your OS), or go to the terminal and press ctrl-C or command-C.

## Features
- A game interface that supports 2 to 3 players, and 1 to 3 human players
- Export replay to file
- Load an existing replay file to watch the game (you may click the buttons or press the left and right arrow keys to navigate through the game)
