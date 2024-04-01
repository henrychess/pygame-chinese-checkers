"""
LoopController class is used to control the game windows displayed.
"""
import os.path
import pygame
import sys
from copy import deepcopy
from bots.GreedyBot0 import GreedyBot0
from bots.GreedyBot1 import GreedyBot1
from bots.GreedyBot2 import GreedyBot2
from game_logic.layout import ALL_COOR
from game_logic.game import Game
from game_logic.helpers import obj_to_subj_coor, setItem
from game_logic.human import Human
from game_logic.player import Player, PlayerMeta
from gui.constants import WIDTH, HEIGHT, WHITE, BLACK, GRAY
from gui.gui_helpers import TextButton, drawBoard, drawPath, highlightMove
from pygame import (
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    KEYDOWN,
    K_LEFT,
    K_RIGHT,
)
from PySide6 import QtWidgets
from time import strftime

# The following is necessary for playerObject = eval(playerClass)() to work
# _ = [
#     GreedyBot0,
#     GreedyBot1,
#     GreedyBot2,
#     RandomBot,
# ]


class LoopController:
    """
    Methods consist of MainLoop, MainMenuLoop, LoadPlayerLoop, GameplayLoop,
    GameOverLoop, ReplayLoop, LoadReplayLoop.
    """

    def __init__(self, waitBot=True, layout="MIRROR", n_pieces=10) -> None:
        # Initialize variables
        self.waitBot = waitBot
        self.n_pieces = n_pieces
        self.layout = layout

        self.loopNum = 0
        self.winnerList = list()
        self.replayRecord = list()
        self.filePath = ""
        self.playerTypes = {}  # e.g. {"GreedyBot1": <class 'bots.GreedyBot0.GreedyBot0'>}
        self.playerNames = None  # e.g. ["Human", "GreedyBot1"]

        # Create a dictionary of player types with PlayerMeta as parent class
        for i in PlayerMeta.playerTypes:
            # key: class name strings, value: class without ()
            self.playerTypes[i.__name__] = i

        # List of all possible player objects
        self.playerList = [
            GreedyBot0(),
            GreedyBot1(),
            GreedyBot2(),
        ]

        # Block all pygame events
        for c_str in pygame.constants.__all__:
            try:
                c_id = eval(f"pygame.{c_str}")
                pygame.event.set_blocked(c_id)
            except (ValueError, TypeError):
                pass

        # Allow only these events
        pygame.event.set_allowed(
            [QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN],
        )

    def mainLoop(self, window: pygame.Surface):
        """
        Controls the flow to enter mainMenuLoop (0), loadPlayerLoop (1),
        gameplayLoop (2), gameOverLoop (3), replayLoop (4), loadReplayLoop (5).
        """
        # print(f"Loop goes on with loopNum {self.loopNum}")

        # First loop to display the main menu
        if self.loopNum == 0:
            self.filePath = False
            self.replayRecord = []
            self.mainMenuLoop(window)

        elif self.loopNum == 1:
            # from playButton in mainMenuLoop
            # enters loadPlayerLoop to choose player types
            self.loadPlayerLoop()

        elif self.loopNum == 2:
            # from startButton in loadPlayerLoop
            # enters gameplayLoop to play the game
            self.winnerList, self.replayRecord = self.gameplayLoop(window)

        elif self.loopNum == 3:
            # from gameplayLoop after a player wins
            self.gameOverLoop(window, self.winnerList, self.replayRecord)

        elif self.loopNum == 4:
            # to view a replay
            # pygame.key.set_repeat(100)
            self.replayLoop(window, self.filePath)

        elif self.loopNum == 5:
            # to select a replay file
            self.filePath = self.loadReplayLoop()

    def mainMenuLoop(self, window: pygame.Surface):
        """
        Display the main menu and register events from the buttons.
        """
        window.fill(WHITE)
        titleText = pygame.font.Font(size=int(WIDTH * 0.08)).render(
            "Chinese Checkers",
            True,
            BLACK,
        )
        titleTextRect = titleText.get_rect()
        titleTextRect.center = (WIDTH * 0.5, HEIGHT * 0.25)
        window.blit(titleText, titleTextRect)
        playButton = TextButton(
            "Play",
            centerx=int(WIDTH * 0.5),
            centery=int(HEIGHT * 0.375),
            width=WIDTH * 0.25,
            height=HEIGHT * 0.125,
            font_size=32,
        )
        loadReplayButton = TextButton(
            "Load replay",
            centerx=int(WIDTH * 0.5),
            centery=int(HEIGHT * 0.625),
            width=WIDTH * 0.25,
            height=HEIGHT * 0.125,
            font_size=32,
        )
        while True:
            # Register close button event
            ev = pygame.event.wait()
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

            # Control flow to the next state
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = ev.type == MOUSEBUTTONDOWN
            if playButton.isClicked(mouse_pos, mouse_left_click):
                # Go to the gamePlayLoop
                self.loopNum = 1
                break
            if loadReplayButton.isClicked(mouse_pos, mouse_left_click):
                # Go to the loadReplayLoop
                self.loopNum = 5
                break

            playButton.draw(window, mouse_pos)
            loadReplayButton.draw(window, mouse_pos)
            pygame.display.update()

    def loadPlayerLoop(self):
        """
        Display a smaller window to select number of players and player types.
        """
        loaded = False
        appModifier = 0.75
        appWidth = WIDTH * appModifier
        appHeight = HEIGHT * appModifier

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        app.aboutToQuit.connect(self.closing)

        Form = QtWidgets.QWidget()
        Form.setWindowTitle("Game Settings")
        Form.resize(appWidth, appHeight)

        box = QtWidgets.QWidget(Form)
        box.setGeometry(
            appWidth * 0.0625,
            appHeight * 0.0625,
            appWidth * 0.875,
            appHeight * 0.625,
        )
        grid = QtWidgets.QGridLayout(box)

        # Choose number of players
        label_pNum = QtWidgets.QLabel(Form)
        label_pNum.setText("No. of Players")

        # Button for 1 player
        rButton_1P = QtWidgets.QRadioButton(Form)
        rButton_1P.setText("1")
        rButton_1P.toggled.connect(
            lambda: label_p2Type.setStyleSheet("color: #878787;"),
        )  # grey out p2 label
        rButton_1P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #878787;"),
        )  # grey out p3 label
        rButton_1P.toggled.connect(lambda: cBox_p2.setDisabled(True))
        rButton_1P.toggled.connect(lambda: cBox_p3.setDisabled(True))
        rButton_1P.toggled.connect(lambda: setItem(self.playerList, 1, None))
        rButton_1P.toggled.connect(lambda: setItem(self.playerList, 2, None))

        # Button for 2 players
        rButton_2P = QtWidgets.QRadioButton(Form)
        rButton_2P.setText("2")
        rButton_2P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #878787;"),
        )  # grey out p3 label
        rButton_2P.toggled.connect(
            lambda: label_p2Type.setStyleSheet("color: #000000;"),
        )  # restore p2 label
        rButton_2P.toggled.connect(lambda: cBox_p2.setDisabled(False))
        rButton_2P.toggled.connect(lambda: cBox_p3.setDisabled(True))
        rButton_2P.toggled.connect(lambda: setItem(self.playerList, 2, None))

        # Button for 3 players
        rButton_3P = QtWidgets.QRadioButton(Form)
        rButton_3P.setText("3")
        rButton_3P.setChecked(True)
        rButton_3P.toggled.connect(
            lambda: label_p2Type.setStyleSheet("color: #000000;"),
        )  # restore p3 label
        rButton_3P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #000000;"),
        )  # restore p3 label
        rButton_3P.toggled.connect(lambda: cBox_p2.setDisabled(False))
        rButton_3P.toggled.connect(lambda: cBox_p3.setDisabled(False))
        rButton_3P.toggled.connect(
            lambda: setItem(
                self.playerList,
                2,
                self.playerTypes[cBox_p3.currentText()](),
            ),
        )

        # Combo boxes for player types
        label_p1Type = QtWidgets.QLabel(Form)
        label_p1Type.setText("Player 1:")
        label_p2Type = QtWidgets.QLabel(Form)
        label_p2Type.setText("Player 2:")
        label_p3Type = QtWidgets.QLabel(Form)
        label_p3Type.setText("Player 3:")
        cBox_p1 = QtWidgets.QComboBox(Form)
        cBox_p2 = QtWidgets.QComboBox(Form)
        cBox_p3 = QtWidgets.QComboBox(Form)
        cBoxes = (cBox_p1, cBox_p2, cBox_p3)

        # Set initial player types for the 3 combo boxes
        if not loaded:
            for i in range(3):
                grid.addWidget(cBoxes[i], i + 1, 2, 1, 2)
                cBoxes[i].addItems(list(self.playerTypes))
                cBoxes[i].setCurrentIndex(i)
            loaded = True

        # Modify playerList when player types are selected
        cBox_p1.currentIndexChanged.connect(
            lambda: setItem(
                self.playerList,
                0,
                self.playerTypes[cBox_p1.currentText()](),
            ),
        )
        cBox_p2.currentIndexChanged.connect(
            lambda: setItem(
                self.playerList,
                1,
                self.playerTypes[cBox_p2.currentText()](),
            ),
        )
        cBox_p3.currentIndexChanged.connect(
            lambda: setItem(
                self.playerList,
                2,
                self.playerTypes[cBox_p3.currentText()](),
            ),
        )

        # Print playerlist for debugging
        rButton_1P.toggled.connect(lambda: print(self.playerList))
        rButton_2P.toggled.connect(lambda: print(self.playerList))
        rButton_3P.toggled.connect(lambda: print(self.playerList))
        cBox_p1.currentIndexChanged.connect(
            lambda: print(self.playerList),
        )
        cBox_p2.currentIndexChanged.connect(
            lambda: print(self.playerList),
        )
        cBox_p3.currentIndexChanged.connect(
            lambda: print(self.playerList),
        )

        # Add widgets to the grid
        grid.addWidget(label_pNum, 0, 0)
        grid.addWidget(rButton_1P, 0, 1)
        grid.addWidget(rButton_2P, 0, 2)
        grid.addWidget(rButton_3P, 0, 3)
        grid.addWidget(label_p1Type, 1, 0, 1, 2)
        grid.addWidget(label_p2Type, 2, 0, 1, 2)
        grid.addWidget(label_p3Type, 3, 0, 1, 2)

        startButton = QtWidgets.QPushButton(Form)
        startButton.setText("Start Game")
        startButton.setGeometry(
            appWidth * 0.625,
            appHeight * 0.8125,
            appWidth * 0.25,
            appHeight * 0.125,
        )
        startButton.clicked.connect(self.startGame)

        cancelButton = QtWidgets.QPushButton(Form)
        cancelButton.setText("Back to Menu")
        cancelButton.setGeometry(
            appWidth * 0.125,
            appHeight * 0.8125,
            appWidth * 0.25,
            appHeight * 0.125,
        )
        cancelButton.clicked.connect(self.backToMenu)

        Form.show()
        app.exec()

    # helpers for loadPlayerLoop and replayLoop
    def startGame(self):
        self.loopNum = 2  # go to gameplay
        while None in self.playerList:
            self.playerList.remove(None)
        self.playerNames = [i.__class__.__name__ for i in self.playerList]
        QtWidgets.QApplication.closeAllWindows()

    # helpers for loadPlayerLoop and replayLoop
    def backToMenu(self):
        self.loopNum = 0  # go to main menu
        QtWidgets.QApplication.closeAllWindows()

    def gameplayLoop(self, window: pygame.Surface):
        """
        Returns:
            [results, replayRecord]
            result : len(n_players-1), list of winning player numbers with
                the 1st winnder at index 0. -1 if draw.
            replayRecord : list of moves in the game.
        """
        # Initialize variables
        playerIndex = 0
        humanPlayerNum = 0
        result = []
        replayRecord = []

        # Set player numbers
        players: list[Player] = deepcopy(self.playerList)
        while None in players:
            players.remove(None)
        for i in range(len(players)):
            players[i].setPlayerNum(i + 1)
        # players: list of player objects selected

        # 1st line: no. of players
        # 2nd line: player names
        # 3rd line: game config
        replayRecord.append(str(len(players)))
        replayRecord.append(",".join(self.playerNames))
        replayRecord.append(f"{self.layout},{self.n_pieces}")

        # Generate the game
        g = Game(players, 1, self.playerNames, self.layout, self.n_pieces)
        oneHuman = exactly_one_is_human(players)
        if oneHuman:
            for player in players:
                if isinstance(player, Human):
                    humanPlayerNum = player.getPlayerNum()

        # Start the game loop
        selectedMove = []  # list of start and end coordinates of picked move
        path = []
        while True:
            currentPlayer = players[playerIndex]

            if self.waitBot:  # wait for user to press a key
                ev = pygame.event.wait()
            else:  # bot moves after waiting
                duration = 500  # milliseconds
                ev = pygame.event.wait(duration)

            # Register close button event
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

            # Draw the board
            window.fill(GRAY)
            drawBoard(g, window)

            # Bot Text
            botText = pygame.font.Font(size=int(HEIGHT * 0.035)).render(
                "Press any key for the bot to make a move",
                antialias=True,
                color=BLACK,
                wraplength=int(WIDTH * 0.2),
            )
            botTextRect = botText.get_rect()
            botTextRect.topright = (WIDTH, 1)
            window.blit(botText, botTextRect)

            # Highlight the 2 coordinates of the move
            highlightMove(g, window, selectedMove)
            drawPath(g, window, path)
            selectedMove = []

            backButton = TextButton(
                "Back to Menu",
                width=int(HEIGHT * 0.25),
                height=int(HEIGHT * 0.0833),
                font_size=int(WIDTH * 0.04),
            )

            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = ev.type == MOUSEBUTTONDOWN

            # Return to main menu if the back button is clicked
            if backButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 0
                return ([], [])
            backButton.draw(window, mouse_pos)
            pygame.display.update()

            # Playing player makes a move
            if isinstance(currentPlayer, Human):
                # Human player makes a move
                start_coor, end_coor = currentPlayer.pickMove(
                    g,
                    window,
                    humanPlayerNum,
                )
                if (not start_coor) and (not end_coor):
                    # Return to main menu
                    self.loopNum = 0
                    return ([], [])
            else:
                # Bot player makes a move
                start_coor, end_coor = currentPlayer.pickMove(g)

            path = g.getMovePath(g.playerNum, start_coor, end_coor)

            g.movePiece(start_coor, end_coor)

            if oneHuman:
                selectedMove = [
                    obj_to_subj_coor(start_coor, humanPlayerNum, self.layout),
                    obj_to_subj_coor(end_coor, humanPlayerNum, self.layout),
                ]
            else:
                selectedMove = [start_coor, end_coor]

            replayRecord.append(str(start_coor) + "to" + str(end_coor))

            # Check if the playing player has won
            winning = g.checkWin(currentPlayer.getPlayerNum())

            if winning:  # and len(players) == 2:
                drawBoard(g, window)
                currentPlayer.has_won = True
                result.append(currentPlayer.getPlayerNum())
                # replayRecord.append(str(currentPlayer.getPlayerNum()))

                # Go to the game over loop
                self.loopNum = 3
                return [result, replayRecord]

            elif winning and len(players) >= 3:
                currentPlayer.has_won = True
                result.append(currentPlayer.getPlayerNum())
                players.remove(currentPlayer)

            # Switch to the next player
            playerIndex = (playerIndex + 1) % len(players)
            g.turnCount += 1
            g.playerNum = playerIndex + 1

    def replayLoop(self, window: pygame.Surface, filePath: str = None):
        # Check if a path has been selected
        if not filePath:
            print("File Path is void!")
            self.loopNum = 0

        # Check validity of replay file
        if (not self.replayRecord) and filePath:
            isValidReplay = True
            move_list = []
            with open(filePath) as f:
                # Parse the file
                text = f.read()
                move_list = text.split("\n")
                playerCount = int(move_list.pop(0))
                playerNames = move_list.pop(0).split(",")
                self.layout, self.n_pieces = move_list.pop(0).split(",")
                self.n_pieces = int(self.n_pieces)
                playerList: list[Player] = []

                # Create player objects
                for i, className in enumerate(playerNames):
                    playerList.append(eval(className)())
                    playerList[-1].setPlayerNum(i + 1)

                # Removed the check for total number of players

                # Check each move is valid
                # Empty line at the end of the file results in an invalid replay
                for i in range(len(move_list)):
                    move_list[i] = move_list[i].split("to")

                    # Check there are 2 sets of coordinates for each move
                    if len(move_list[i]) != 2:
                        print(i, move_list[i])
                        self.showNotValidReplay()
                        isValidReplay = False
                        break
                    for j in range(len(move_list[i])):
                        move_list[i][j] = eval(move_list[i][j])

                        # Check coordinates are tuples
                        if not isinstance(move_list[i][j], tuple):
                            print(f"Invalid coordinates: {move_list[i][j]}")
                            self.showNotValidReplay()
                            isValidReplay = False
                            break
                        # Check if the coordinates exists on the board
                        if move_list[i][j] not in ALL_COOR:
                            print(f"Invalid coordinates: {move_list[i][j]}")
                            self.showNotValidReplay()
                            isValidReplay = False
                            break

            if isValidReplay:
                self.replayRecord = move_list

        # Start the replay if it is valid
        if self.replayRecord:
            if f:
                del f
            if text:
                del text

            # Initialise game
            path = None
            g = Game(playerList, 1, playerNames, self.layout, self.n_pieces)
            g.playerNum = 0
            g.turnCount = 0

            # Set up UI buttons
            prevButton = TextButton(
                "<",
                centerx=WIDTH * 0.125,
                centery=HEIGHT * 0.5,
                width=int(WIDTH / 8),
                height=int(HEIGHT / 6),
                font_size=int(WIDTH * 0.04),
            )
            nextButton = TextButton(
                ">",
                centerx=WIDTH * 0.875,
                centery=HEIGHT * 0.5,
                width=int(WIDTH / 8),
                height=int(HEIGHT / 6),
                font_size=int(WIDTH * 0.04),
            )
            backButton = TextButton(
                "Back to Menu",
                width=int(HEIGHT * 0.25),
                height=int(HEIGHT * 0.0833),
                font_size=int(WIDTH * 0.04),
            )
            autoPlayButton = TextButton(
                "Auto Play",
                centerx=WIDTH * 0.875,
                centery=HEIGHT * 0.875,
                width=int(WIDTH / 9),
                height=int(HEIGHT / 10),
                font_size=int(WIDTH * 0.03),
            )
            # BUG: requires double click to actiate autoPlay
            hintText = pygame.font.Font(size=int(HEIGHT * 0.03)).render(
                "Use the buttons or the left and right arrow keys to navigate through the game",
                antialias=True,
                color=BLACK,
                wraplength=int(WIDTH * 0.375),
            )
            hintTextRect = hintText.get_rect()
            hintTextRect.topright = (WIDTH, 1)

            def previousMove():
                nonlocal g, moveListIndex, selectedMove, path
                g.playerNum = g.turnCount % playerCount + 1
                g.turnCount -= 1
                moveListIndex -= 1
                start_coor = move_list[moveListIndex + 1][1]
                end_coor = move_list[moveListIndex + 1][0]
                path = g.getMovePath(g.playerNum, start_coor, end_coor)
                g.movePiece(start_coor, end_coor)
                selectedMove = move_list[moveListIndex] if moveListIndex >= 0 else []

            def nextMove():
                nonlocal g, moveListIndex, selectedMove, path
                g.playerNum = g.turnCount % playerCount + 1
                g.turnCount += 1
                moveListIndex += 1
                start_coor = move_list[moveListIndex][0]
                end_coor = move_list[moveListIndex][1]
                path = g.getMovePath(g.playerNum, start_coor, end_coor)
                g.movePiece(start_coor, end_coor)
                selectedMove = move_list[moveListIndex]

            # Initialise replay variables
            moveListIndex = -1
            selectedMove = []
            left = False
            right = False
            mouse_left_click = False
            autoPlay = False
            autoPlayButton.enabled = True

            # Iterate through all the moves
            while True:
                # Register mouse left click event
                mouse_pos = pygame.mouse.get_pos()

                # Wait for user to press a key
                if not autoPlay:
                    ev = pygame.event.wait()
                    # Register mouse click and key press events
                    mouse_left_click = ev.type == MOUSEBUTTONDOWN
                    left = (
                        ev.type == KEYDOWN and ev.key == K_LEFT and prevButton.enabled
                    )
                    right = (
                        ev.type == KEYDOWN and ev.key == K_RIGHT and nextButton.enabled
                    )
                    autoPlay = autoPlayButton.isClicked(
                        mouse_pos,
                        mouse_left_click,
                    )
                    if autoPlay:
                        print("[gui.loops] Automatically replaying...")
                # Replay automatically after waiting
                if autoPlay:
                    duration = 500  # milliseconds
                    ev = pygame.event.wait(duration)
                    mouse_left_click = ev.type == MOUSEBUTTONDOWN
                    right = True

                # Register close button event
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()

                # Enable/disable buttons at beginning/end of replay
                if moveListIndex == -1:
                    prevButton.enabled = False
                else:
                    prevButton.enabled = True
                if moveListIndex == len(move_list) - 1:
                    # Stop automatic replay
                    autoPlay = False
                    nextButton.enabled = False
                    right = False
                    print("[gui.loops] End of replay")
                else:
                    nextButton.enabled = True

                # Exit replay mode
                if backButton.isClicked(mouse_pos, mouse_left_click):
                    self.loopNum = 0
                    break
                # Reverse move
                if prevButton.isClicked(mouse_pos, mouse_left_click) or left:
                    previousMove()
                # Move to next move
                if nextButton.isClicked(mouse_pos, mouse_left_click) or right:
                    nextMove()

                # Draw buttons and board
                window.fill(GRAY)
                window.blit(hintText, hintTextRect)
                drawBoard(g, window)
                highlightMove(g, window, selectedMove)
                drawPath(g, window, path)
                prevButton.draw(window, mouse_pos)
                nextButton.draw(window, mouse_pos)
                backButton.draw(window, mouse_pos)
                autoPlayButton.draw(window, mouse_pos)
                pygame.display.update()

    def loadReplayLoop(self):
        """
        Display a smaller window to select a replay file.
        """
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        app.aboutToQuit.connect(self.closing)

        if not os.path.isdir("./replays"):
            os.mkdir("./replays")
        filePath = QtWidgets.QFileDialog.getOpenFileName(
            dir="./replays",
            filter="*.txt",
        )[0]
        if filePath:
            self.loopNum = 4
            return filePath
        else:  # User cancelled
            self.loopNum = 0
            return False

    def gameOverLoop(
        self,
        window: pygame.Surface,
        winnerList: list,
        replayRecord: list,
    ):
        # print(winnerList); print(replayRecord)
        # winner announcement text
        if len(winnerList) == 1:
            winnerString = "Player %d wins" % winnerList[0]
        elif len(winnerList) == 2:
            winnerString = "Player %d wins, then Player %d wins" % (
                winnerList[0],
                winnerList[1],
            )
        else:
            winnerString = "len(winnerList) is %d" % len(winnerList)
        font = pygame.font.SysFont("Arial", int(WIDTH * 0.04))
        text = font.render(winnerString, True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (int(WIDTH * 0.5), int(HEIGHT / 6))
        window.blit(text, textRect)

        # Create buttons
        menuButton = TextButton(
            "Back to menu",
            centerx=int(WIDTH * 0.25),
            centery=int(HEIGHT * 2 / 3),
            font_size=32,
        )
        exportReplayButton = TextButton(
            "Export replay",
            centerx=int(WIDTH * 0.75),
            centery=int(HEIGHT * 2 / 3),
            font_size=32,
        )

        while True:
            # Register events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = pygame.mouse.get_pressed()[0]

            # Return to main menu
            if menuButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 0
                break

            # Export replay
            if exportReplayButton.isClicked(mouse_pos, mouse_left_click):
                curTime = strftime("%Y%m%d-%H%M%S")
                if not os.path.isdir("./replays"):
                    os.mkdir("./replays")
                with open(f"./replays/replay-{curTime}.txt", mode="w+") as f:
                    for i in range(len(replayRecord)):
                        if i < len(replayRecord) - 1:
                            f.write(str(replayRecord[i]) + "\n")
                        else:
                            f.write(str(replayRecord[i]))
                exportReplayButton.text = "Replay exported!"
                exportReplayButton.enabled = False

            # Draw buttons
            menuButton.draw(window, mouse_pos)
            exportReplayButton.draw(window, mouse_pos)
            pygame.display.update()

    def closing(self):
        if self.loopNum == 0 or self.loopNum == 1:
            self.backToMenu()
        elif self.loopNum == 2:
            self.startGame()

    def showNotValidReplay(self):
        print("This is not a valid replay!")
        self.loopNum = 0


def exactly_one_is_human(players: list[Player]):
    """
    Checks through the list of players to see if exactly one of them is human.
    """
    only_one = False
    for player in players:
        if only_one is False and isinstance(player, Human):
            only_one = True
        elif only_one is True and isinstance(player, Human):
            return False
    return only_one


def trainingLoop(g: Game, players: list[Player], recordReplay: bool = False):
    """
    Not sure what this does. Currently not used.
    """
    playerIndex = 0
    replayRecord = []
    if recordReplay:
        replayRecord.append(str(len(players)))

    # Ensure no humans are playing
    for player in players:
        assert not isinstance(player, Human), (
            "Can't have humans during training! Human at player %d"
            % players.index(player)
            + 1
        )

    for i in range(len(players)):
        players[i].setPlayerNum(i + 1)

    # Main training game loop
    while True:
        currentPlayer = players[playerIndex]

        # Playing player makes a move
        start_coor, end_coor = currentPlayer.pickMove(g)
        g.movePiece(start_coor, end_coor)

        if recordReplay:
            replayRecord.append(str(start_coor) + " " + str(end_coor))

        winning = g.checkWin(currentPlayer.getPlayerNum())

        if winning and len(players) == 2:
            currentPlayer.has_won = True
            print("The winner is Player %d" % currentPlayer.getPlayerNum())
            print(f"{len(replayRecord)} moves")
            break  # TODO: return stuff?
        elif winning and len(players) == 3:
            currentPlayer.has_won = True
            players.remove(currentPlayer)
            print(
                "The first winner is Player %d" % currentPlayer.getPlayerNum(),
            )
        if playerIndex >= len(players) - 1:
            playerIndex = 0
        else:
            playerIndex += 1
