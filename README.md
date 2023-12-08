# pygame-chinese-checkers

> [!NOTE]
> This is a hobby project by a beginner/amateur in programming. You may encounter bugs. If you do, please report them.


> [!CAUTION]
> This game is not tested in Linux environments. Theoretically it should run, but users have reported otherwise.

## Rules

Chinese Checkers, or Sternhalma, is a turn-based board game of German origin. [Here](https://en.wikipedia.org/wiki/Chinese_checkers) is the Wikipedia page of the game. (No, really, it's not of Chinese origin. It was named that way to promote sales. 😛) The version used in this program supports 2 to 3 players, with each player using 15 pieces. In a 2-player game, the pieces do not start in the opposite sides.

The rules of the game are simple: be the first to move all your pieces to the triangular area at the opposite side. Each turn, you move a piece in one of the following two ways: move it to an adjacent empty spot, or make it hop over one and only one piece of any color. If you make the piece hop, you may make it hop again any number of times in the same turn. Be careful: you cannot end your turn with a piece on a spot that is neither in your territory nor in the neutral zone. You may pass enemy territories without having the piece end up staying there, though. (This can only happen when you're hopping.) In this program, turns alternate clockwise. (Geometrically, it doesn't matter if it's clockwise or counterclockwise. This is an arbitrary choice.)

The following image is an example of a hop. The highlighted green piece may hop as the arrows indicate, and may end in any of the spots except for the one marked with an X (as it's in the red player's territory).

<img src="https://github.com/henrychess/pygame-chinese-checkers/blob/main/images/hop-example.png" height=200>

## Features
- A game interface that supports 2 to 3 players. Any of them can be a human player.
- Export replay to file
- Load an existing replay file to watch the game (you may click the buttons or press the left and right arrow keys to navigate through the game)
- You may create **custom bots** under the `custom_bots` folder! It'll automatically be added into the game. For more information, check out the [custom bot guide](https://github.com/henrychess/pygame-chinese-checkers/blob/main/custom_bots/README.md).

## Showcase video

### Most Recent Showcase:

[Nov 25, 2023 build](https://youtu.be/r3i92YeDN2w)

### Older Showcase Vids
[Nov 6, 2023 build](https://youtu.be/zsmd8o0BoDw)

## Requirements
- Python 3.9+
- `pygame-ce` and `PySide6`

### Installing Python (without Anaconda)

To install Python itself, head to the [official website](https://www.python.org/) and follow their instructions.
You may also check your Python version by pasting this in your terminal:
```
python --version
```
If you're on Linux/Mac and you have multiple versions of Python, you can specify the Python version you're using. Instead of simply `python`, you can instead use:
```
python3.10 [options]...
```
or whatever version your Python is.

### Installing Python within an Anaconda environment

[Anaconda](https://www.anaconda.com/) is a great tool if you want to install many versions of Python in your computer. Anaconda environments do not interfere with each other. To install Anaconda, head to their official website and follow the instructions. After you have Anaconda installed, you may check your current environments in a terminal like so: (`conda` commands are the same across Windows and UNIX-like OSes)
```
conda env list
```
To activate an environment, use:
```
conda activate [env_name]
```
To create a new environment, use the `conda create` command. The following example creates an environment with name `py3.12` and installs Python version 3.12 upon its creation:
```
conda create -n py3.12 python=3.12
```

### Installing the Python packages

Once you have confirmed you have the right Python version, and optionally the right Conda environment, install `pygame-ce` and `PySide6`. To do this, paste this into your terminal:
```
python -m pip install -U pygame-ce PySide6
```

## Running the program
To run it, first open a terminal at the folder where this project is saved at, or use the `cd` command in the terminal.
The command on Linux/Mac should look like this:
```
cd path/to/your/folder
```
On Windows, use this:
```
cd /d path\to\your\folder
```
The path to your folder may be copied from certain file managing programs or typed by hand. It's easier to just copy the path if you're on Windows though.

When your working directory is where the game is stored, use:
```
python main.py
```
to start the game. If nothing goes wrong, the game should prompt you to select players after clicking Play.

If you want to close the window, you have to manually quit the game by clicking the X button on the top right corner (or top left, depending on your OS), or go to the terminal and press ctrl-C or command-C.
