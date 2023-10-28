from .game import *
from .player import *
from .helpers import *
import sys
import pygame
from pygame.locals import *
from PySide6 import QtWidgets

class LoopController:
    
    def __init__(self) -> None:
        self.loopNum = 0
        self.winnerList = list()
        self.replayRecord = list()
        self.playerStrList = [
            "HumanPlayer",
            "RandomBotPlayer",
            "GreedyRandomBotPlayer",
            "Greedy1BotPlayer",
            "Greedy2BotPlayer"
        ]
        self.playerList = [
            eval(f"{self.playerStrList[0]}()",),
            eval(f"{self.playerStrList[1]}()",),
            eval(f"{self.playerStrList[2]}()",)
        ]
        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    def mainLoop(self, window: pygame.Surface):
        print(f"Loop goes on with loopNum {self.loopNum}")
        if self.loopNum == 0:
            self.mainMenuLoop(window)
        elif self.loopNum == 1:
            self.loadPlayerLoop()
        elif self.loopNum == 2:
            self.winnerList, self.replayRecord = self.gameplayLoop(
                window, self.playerList)
        elif self.loopNum == 3:
            self.gameOverLoop(window, self.winnerList, self.replayRecord)

    def gameplayLoop(self, window: pygame.Surface, players: list[Player]):
        playingPlayerIndex = 0
        humanPlayerNum = 0
        #returnStuff[0] is the winning player number
        #returnStuff[1] is replayRecord
        #if there are two players, len(returnStuff[0]) is 1
        #otherwise, it is 2, with the first winner at index 0
        returnStuff = [[],[]]
        replayRecord = []
        #replayRecord[0] marks the number of players
        while None in players: players.remove(None)
        if len(players) > 3: players = players[:3]
        players[0].setPlayerNum(1)
        players[1].setPlayerNum(2)
        if len(players) == 3: players[2].setPlayerNum(3)
        #generate the Game
        g = Game(len(players))
        #some other settings
        replayRecord.append(str(len(players)))
        if exactly_one_is_human(players):
            for player in players:
                if isinstance(player, HumanPlayer):
                    humanPlayerNum = player.getPlayerNum()
        #start the game loop
        while True:
            window.fill(GRAY)
            if humanPlayerNum != 0:
                g.drawBoard(window, humanPlayerNum)
            else: 
                g.drawBoard(window)
            pygame.display.update()
            playingPlayer = players[playingPlayerIndex]
            if isinstance(playingPlayer, HumanPlayer):
                start_coor, end_coor = playingPlayer.pickMove(g, window, humanPlayerNum)
            else:
                start_coor, end_coor = playingPlayer.pickMove(g)
            g.movePiece(start_coor, end_coor)
            replayRecord.append(str(start_coor)+'to'+str(end_coor))
            winning = g.checkWin(playingPlayer.getPlayerNum())
            if winning and len(players) == 2:
                if humanPlayerNum != 0:
                    g.drawBoard(window, humanPlayerNum)
                else: 
                    g.drawBoard(window)
                playingPlayer.has_won = True
                returnStuff[0].append(playingPlayer.getPlayerNum())
                print('The winner is Player %d' % playingPlayer.getPlayerNum())
                returnStuff[1] = replayRecord
                self.loopNum = 3
                #print(returnStuff)
                return returnStuff
            elif winning and len(players) == 3:
                playingPlayer.has_won = True
                returnStuff[0].append(playingPlayer.getPlayerNum())
                players.remove(playingPlayer)
                #TODO: show the message on screen
                print("The first winner is Player %d" % playingPlayer.getPlayerNum())
            if playingPlayerIndex >= len(players) - 1: playingPlayerIndex = 0
            else: playingPlayerIndex += 1

    def trainingLoop(self, g: Game, players: list[Player], recordReplay: bool=False):
        playingPlayerIndex = 0
        replayRecord = []
        if recordReplay:
            replayRecord.append(str(len(players)))
        for player in players:
            assert not isinstance(player, HumanPlayer), "Can't have humans during training! Human at player %d" % players.index(player) + 1
        while True:
            playingPlayer = players[playingPlayerIndex]
            start_coor, end_coor = playingPlayer.pickMove(g)
            g.movePiece(start_coor, end_coor)
            if recordReplay:
                replayRecord.append(str(start_coor)+' '+str(end_coor))
            winning = g.checkWin(playingPlayer.getPlayerNum())
            if winning and len(players) == 2:
                playingPlayer.has_won = True
                #TODO: show the message on screen
                print('The winner is Player %d' % playingPlayer.getPlayerNum())
                break
                #TODO: return stuff
            elif winning and len(players) == 3:
                playingPlayer.has_won = True
                players.remove(playingPlayer)
                #TODO: show the message on screen
                print("The first winner is Player %d" % playingPlayer.getPlayerNum())
            if playingPlayerIndex >= len(players) - 1: playingPlayerIndex = 0
            else: playingPlayerIndex += 1

    def replayLoop(self, window: pygame.Surface):
        pass #TODO

    def gameOverLoop(self, window: pygame.Surface, winnerList: list, replayRecord: list):
        #print(winnerList); print(replayRecord)
        #winner announcement text
        if len(winnerList) == 1:
            winnerString = 'Player %d wins' % winnerList[0]
        elif len(winnerList) == 2:
            winnerString = 'Player %d wins, then Player %d wins' % (winnerList[0], winnerList[1])
        else:
            winnerString = 'len(winnerList) is %d' % len(winnerList)
        font = pygame.font.SysFont('Arial', 32)
        text = font.render(winnerString, True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (400,100)
        window.blit(text, textRect)
        #TODO: buttons
        menuButton = TextButton("Back to menu", x=100, y=400)
        exportReplayButton = TextButton("Export replay", x=500, y=400)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = pygame.mouse.get_pressed()[0]
            if menuButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 0
                break
            if exportReplayButton.isClicked(mouse_pos, mouse_left_click):
                with open("./replays/replay.txt", mode="w+") as f:
                    for i in replayRecord:
                        f.write(str(i)+'\n')
                exportReplayButton.text = "Replay exported!"
                exportReplayButton.enabled = False
            menuButton.draw(window, mouse_pos, mouse_left_click)
            exportReplayButton.draw(window, mouse_pos, mouse_left_click)
            pygame.display.update()

    def loadPlayerLoop(self):
        #print(self.playerList)
        appModifier = 0.75
        appWidth = WIDTH * appModifier
        appHeight = HEIGHT * appModifier
        #
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        app.aboutToQuit.connect(self.closing)
        Form = QtWidgets.QWidget()
        Form.setWindowTitle("Game Settings")
        Form.resize(appWidth, appHeight)
        #
        box = QtWidgets.QWidget(Form)
        box.setGeometry(
            appWidth * 0.0625, appHeight * 0.0625,
            appWidth * 0.875, appHeight * 0.625)
        grid = QtWidgets.QGridLayout(box)
        #
        label_pNum = QtWidgets.QLabel(Form)
        label_pNum.setText("Number of Players")
        rButton_2P = QtWidgets.QRadioButton(Form)
        rButton_2P.setText('2')
        rButton_2P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #878787;"))
        rButton_2P.toggled.connect(
            lambda: cBox_p3.setDisabled(True))
        rButton_2P.toggled.connect(
            lambda: setItem(self.playerList, 2, None))
        rButton_2P.toggled.connect(
            lambda: print(self.playerList))
        rButton_3P = QtWidgets.QRadioButton(Form)
        rButton_3P.setText('3')
        rButton_3P.setChecked(True)
        rButton_3P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #000000;"))
        rButton_3P.toggled.connect(
            lambda: cBox_p3.setDisabled(False))
        rButton_3P.toggled.connect(
            lambda: setItem(self.playerList, 2, 
            eval(f"{self.playerStrList[cBox_p3.currentIndex()]}()")))
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
        
        for i in range(3):
            grid.addWidget(cBoxes[i], i+1, 2, 1, 2)
            cBoxes[i].addItems(self.playerStrList)
            cBoxes[i].setCurrentIndex(i)

        cBox_p1.currentIndexChanged.connect(
            lambda: setItem(self.playerList, 0, eval(f"{self.playerStrList[i]}()")))
        cBox_p1.currentIndexChanged.connect(
            lambda: print(self.playerList))
        cBox_p2.currentIndexChanged.connect(
            lambda: setItem(self.playerList, 1, eval(f"{self.playerStrList[i]}()")))
        cBox_p2.currentIndexChanged.connect(
            lambda: print(self.playerList))
        cBox_p3.currentIndexChanged.connect(
            lambda: setItem(self.playerList, 2, eval(f"{self.playerStrList[i]}()")))
        cBox_p3.currentIndexChanged.connect(
            lambda: print(self.playerList))
        #
        grid.addWidget(label_pNum, 0, 0, 1, 2)
        grid.addWidget(rButton_2P, 0, 2)
        grid.addWidget(rButton_3P, 0, 3)
        grid.addWidget(label_p1Type, 1, 0, 1, 2)
        grid.addWidget(label_p2Type, 2, 0, 1, 2)
        grid.addWidget(label_p3Type, 3, 0, 1, 2)
        #
        startButton = QtWidgets.QPushButton(Form)
        startButton.setText("Start Game")
        startButton.setGeometry(
            appWidth * 0.625, appHeight * 0.8125,
            appWidth * 0.25, appHeight * 0.125
        )
        startButton.clicked.connect(self.startGame)
        #
        cancelButton = QtWidgets.QPushButton(Form)
        cancelButton.setText("Back to Menu")
        cancelButton.setGeometry(
            appWidth * 0.125, appHeight * 0.8125,
            appWidth * 0.25, appHeight * 0.125
        )
        cancelButton.clicked.connect(self.backToMenu)
        #
        Form.show()
        app.exec()
    
    #helpers for loadGame
    def startGame(self):
        print(self.playerList)
        self.loopNum = 2 #go to gameplay
        QtWidgets.QApplication.closeAllWindows()
    def backToMenu(self):
        self.loopNum = 0 #go to main menu
        QtWidgets.QApplication.closeAllWindows()
    def closing(self):
        if self.loopNum == 0 or self.loopNum == 1: self.backToMenu()
        elif self.loopNum == 2: self.startGame()

    def mainMenuLoop(self, window:pygame.Surface):
        window.fill(WHITE)
        playButton = TextButton(
            "Play", 350, 200, 150, 70, font_size=32)
        loadReplayButton = TextButton(
            "Load replay", 350, 400, 150, 70, font_size=32)
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = pygame.mouse.get_pressed()[0]
            if playButton.isClicked(mouse_pos, mouse_left_click):
                print("play")
                self.loopNum = 1
                break
                #TODO: loadPlayerLoop
            if loadReplayButton.isClicked(mouse_pos, mouse_left_click):
                print('test')
                #
                """ file_path = prompt_file()
                if not file_path:
                    print('file path is empty')
                else:
                    print(file_path) """

            playButton.draw(window, mouse_pos, mouse_left_click)
            loadReplayButton.draw(window, mouse_pos, mouse_left_click)
            pygame.display.update()

def exactly_one_is_human(players: list[Player]):
    b = False
    for player in players:
        if b == False and isinstance(player, HumanPlayer):
            b = True
        elif b == True and isinstance(player, HumanPlayer):
            return False
    return b
