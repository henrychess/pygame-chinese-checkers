from .game import *
from .player import *
from .helpers import *
import sys, os.path
import pygame
from pygame.locals import *
from PySide6 import QtWidgets
from time import strftime
from custom_bots import *

class LoopController:
    
    def __init__(self) -> None:
        self.loopNum = 0
        self.winnerList = list()
        self.replayRecord = list()
        self.playerTypes = {}
        self.filePath = ''
        # key: class name strings
        # value: class without ()
        for i in PlayerMeta.playerTypes:
            self.playerTypes[i.__name__] = i
        self.playerList = [
            HumanPlayer(),
            Greedy1BotPlayer(),
            Greedy2BotPlayer()
        ]
        pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])

    def mainLoop(self, window: pygame.Surface):
        # print(f"Loop goes on with loopNum {self.loopNum}")
        if self.loopNum == 0:
            self.playerList = [
                HumanPlayer(),
                Greedy1BotPlayer(),
                Greedy2BotPlayer()
            ]
            pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
            self.filePath = False
            self.replayRecord = []
            self.mainMenuLoop(window)
        elif self.loopNum == 1:
            self.loadPlayerLoop()
        elif self.loopNum == 2:
            self.winnerList, self.replayRecord = self.gameplayLoop(
                window, self.playerList)
        elif self.loopNum == 3:
            self.gameOverLoop(window, self.winnerList, self.replayRecord)
        elif self.loopNum == 4:
            pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN])
            pygame.key.set_repeat(100)
            self.replayLoop(window, self.filePath)
        elif self.loopNum == 5:
            self.filePath = self.loadReplayLoop()

    def gameplayLoop(self, window: pygame.Surface, playerss: list[Player]):
        playingPlayerIndex = 0
        humanPlayerNum = 0
        #returnStuff[0] is the winning player number,
        #or -1 if it's a draw
        #returnStuff[1] is replayRecord
        #if there are two players, len(returnStuff[0]) is 1
        #otherwise, it is 2, with the first winner at index 0
        returnStuff = [[],[]]
        replayRecord = []
        #replayRecord[0] marks the number of players
        players = copy.deepcopy(playerss)
        while None in players: players.remove(None)
        if len(players) > 3: players = players[:3]
        players[0].setPlayerNum(1)
        players[1].setPlayerNum(2)
        if len(players) == 3: players[2].setPlayerNum(3)
        #generate the Game
        g = Game(len(players))
        #some other settings
        replayRecord.append(str(len(players)))
        oneHuman = exactly_one_is_human(players)
        if oneHuman:
            for player in players:
                if isinstance(player, HumanPlayer):
                    humanPlayerNum = player.getPlayerNum()
        highlight = []
        #start the game loop
        while True:
            playingPlayer = players[playingPlayerIndex]
            # If 100 milliseconds (0.1 seconds) have passed
            # and there is no event, ev will be NOEVENT and
            # the bot player will make a move.
            # Otherwise, the bot player won't move until you
            # move your mouse.
            ev = pygame.event.wait(100)
            if ev.type == QUIT: pygame.quit(); sys.exit()
            window.fill(GRAY)
            if humanPlayerNum != 0:
                g.drawBoard(window, humanPlayerNum)
            else: 
                g.drawBoard(window)
            if highlight:
                pygame.draw.circle(window, (117,10,199), abs_coors(g.centerCoor, highlight[0], g.unitLength), g.circleRadius, g.lineWidth+2)
                pygame.draw.circle(window, (117,10,199), abs_coors(g.centerCoor, highlight[1], g.unitLength), g.circleRadius, g.lineWidth+2)
            backButton = TextButton('Back to Menu', width=int(HEIGHT*0.25), height=int(HEIGHT*0.0833), font_size=int(WIDTH*0.04))
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = ev.type == MOUSEBUTTONDOWN
            if backButton.isClicked(mouse_pos, mouse_left_click):
                self.loopNum = 0
                return ([], [])
            backButton.draw(window, mouse_pos)
            pygame.display.update()
            if isinstance(playingPlayer, HumanPlayer):
                start_coor, end_coor = playingPlayer.pickMove(g, window, humanPlayerNum, highlight)
                if (not start_coor) and (not end_coor):
                    self.loopNum = 0
                    return ([], [])
            else:
                start_coor, end_coor = playingPlayer.pickMove(g)
            g.movePiece(start_coor, end_coor)
            if oneHuman: highlight = [obj_to_subj_coor(start_coor, humanPlayerNum), obj_to_subj_coor(end_coor, humanPlayerNum)]
            else: highlight = [start_coor, end_coor]
            replayRecord.append(str(start_coor)+'to'+str(end_coor))
            winning = g.checkWin(playingPlayer.getPlayerNum())
            if winning and len(players) == 2:
                if humanPlayerNum != 0:
                    g.drawBoard(window, humanPlayerNum)
                else: 
                    g.drawBoard(window)
                playingPlayer.has_won = True
                returnStuff[0].append(playingPlayer.getPlayerNum())
                # print('The winner is Player %d' % playingPlayer.getPlayerNum())
                returnStuff[1] = replayRecord
                self.loopNum = 3
                #print(returnStuff)
                return returnStuff
            elif winning and len(players) == 3:
                playingPlayer.has_won = True
                returnStuff[0].append(playingPlayer.getPlayerNum())
                players.remove(playingPlayer)
                #TODO: show the message on screen
                # print("The first winner is Player %d" % playingPlayer.getPlayerNum())
            if playingPlayerIndex >= len(players) - 1: playingPlayerIndex = 0
            else: playingPlayerIndex += 1

    def replayLoop(self, window: pygame.Surface, filePath: str = None):
        if not filePath:
            print("File Path is void!")
            self.loopNum = 0
        if (not self.replayRecord) and filePath:
            isValidReplay = True
            move_list = []
            with open(filePath) as f:
                text = f.read()
                move_list = text.split('\n')
                playerCount = move_list.pop(0)
                if not eval(playerCount) in (2, 3):
                    self.showNotValidReplay()
                    isValidReplay = False
                else:
                    playerCount = eval(playerCount)
                    for i in range(len(move_list)):
                        move_list[i] = move_list[i].split("to")
                        if (len(move_list[i]) != 2):
                            self.showNotValidReplay()
                            isValidReplay = False
                            break
                        else:
                            for j in range(len(move_list[i])):
                                move_list[i][j] = eval(move_list[i][j])
                                if not isinstance(move_list[i][j], tuple):
                                    self.showNotValidReplay()
                                    isValidReplay = False
                                    break
            for i in range(len(move_list)):
                if move_list[i][0] not in ALL_COOR or move_list[i][1] not in ALL_COOR:
                    self.showNotValidReplay()
                    isValidReplay = False
                    break
            if isValidReplay: self.replayRecord = [playerCount] + move_list
        if self.replayRecord:
            if f: del f
            if text: del text
            playerCount = self.replayRecord.pop(0)
            g = Game(playerCount)
            prevButton = TextButton('<', centerx=WIDTH*0.125, centery=HEIGHT*0.5, width=int(WIDTH/8), height=int(HEIGHT/6), font_size=int(WIDTH*0.04))
            nextButton = TextButton('>', centerx=WIDTH*0.875, centery=HEIGHT*0.5, width=int(WIDTH/8), height=int(HEIGHT/6), font_size=int(WIDTH*0.04))
            backButton = TextButton('Back to Menu', width=int(HEIGHT*0.25), height=int(HEIGHT*0.0833), font_size=int(WIDTH*0.04))
            moveListIndex = -1
            left = False; right = False
            highlight = []
            window.fill(WHITE)
            hintText = pygame.font.Font(size=int(HEIGHT*0.05)).render(
                "Use the buttons or the left and right arrow keys to navigate through the game",
                antialias=True, color=BLACK, wraplength=int(WIDTH*0.375))
            hintTextRect = hintText.get_rect()
            hintTextRect.topright = (WIDTH, 1)
            window.blit(hintText, hintTextRect)
            while True:
                ev = pygame.event.wait()
                if ev.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if moveListIndex == -1: prevButton.enabled = False
                else: prevButton.enabled = True
                if moveListIndex == len(move_list) - 1: nextButton.enabled = False
                else: nextButton.enabled = True
                mouse_pos = pygame.mouse.get_pos()
                mouse_left_click = ev.type == MOUSEBUTTONDOWN
                left = ev.type == KEYDOWN and ev.key == K_LEFT and prevButton.enabled
                right = ev.type == KEYDOWN and ev.key == K_RIGHT and nextButton.enabled
                if backButton.isClicked(mouse_pos, mouse_left_click):
                    self.loopNum = 0
                    break
                if prevButton.isClicked(mouse_pos, mouse_left_click) or left:
                    moveListIndex -= 1
                    # reverse-move move_list[moveListIndex + 1]
                    g.movePiece(move_list[moveListIndex + 1][1], move_list[moveListIndex + 1][0])
                    highlight = move_list[moveListIndex] if moveListIndex >= 0 else []
                if nextButton.isClicked(mouse_pos, mouse_left_click) or right:
                    moveListIndex += 1
                    # move move_list[moveListIndex]
                    g.movePiece(move_list[moveListIndex][0], move_list[moveListIndex][1])
                    highlight = move_list[moveListIndex]
                prevButton.draw(window, mouse_pos)
                nextButton.draw(window, mouse_pos)
                backButton.draw(window, mouse_pos)
                g.drawBoard(window)
                if highlight:
                    pygame.draw.circle(window, (117,10,199), abs_coors(g.centerCoor, highlight[0], g.unitLength), g.circleRadius, g.lineWidth+2)
                    pygame.draw.circle(window, (117,10,199), abs_coors(g.centerCoor, highlight[1], g.unitLength), g.circleRadius, g.lineWidth+2)
                pygame.display.update()

    def loadReplayLoop(self):
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()
        if not os.path.isdir("./replays"): os.mkdir("./replays")
        filePath = QtWidgets.QFileDialog.getOpenFileName(dir="./replays", filter="*.txt")[0]
        if filePath:
            # print(filePath)
            self.loopNum = 4
            return filePath
        else:
            # print("cancelled")
            self.loopNum = 0
            return False

    def gameOverLoop(self, window: pygame.Surface, winnerList: list, replayRecord: list):
        #print(winnerList); print(replayRecord)
        #winner announcement text
        if len(winnerList) == 1:
            winnerString = 'Player %d wins' % winnerList[0]
        elif len(winnerList) == 2:
            winnerString = 'Player %d wins, then Player %d wins' % (winnerList[0], winnerList[1])
        else:
            winnerString = 'len(winnerList) is %d' % len(winnerList)
        font = pygame.font.SysFont('Arial', int(WIDTH*0.04))
        text = font.render(winnerString, True, BLACK, WHITE)
        textRect = text.get_rect()
        textRect.center = (int(WIDTH*0.5),int(HEIGHT/6))
        window.blit(text, textRect)
        #buttons
        menuButton = TextButton("Back to menu", centerx=int(WIDTH*0.25), centery=int(HEIGHT*2/3))
        exportReplayButton = TextButton("Export replay", centerx=int(WIDTH*0.75), centery=int(HEIGHT*2/3))
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
                curTime = strftime("%Y%m%d-%H%M%S")
                if not os.path.isdir("./replays"): os.mkdir("./replays")
                with open(f"./replays/replay-{curTime}.txt", mode="w+") as f:
                    for i in range(len(replayRecord)):
                        if i < len(replayRecord) - 1: f.write(str(replayRecord[i])+'\n')
                        else: f.write(str(replayRecord[i]))
                exportReplayButton.text = "Replay exported!"
                exportReplayButton.enabled = False
            menuButton.draw(window, mouse_pos)
            exportReplayButton.draw(window, mouse_pos)
            pygame.display.update()

    def loadPlayerLoop(self):
        loaded = False
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
        # rButton_2P.toggled.connect(
        #     lambda: print(self.playerList))
        rButton_3P = QtWidgets.QRadioButton(Form)
        rButton_3P.setText('3')
        rButton_3P.setChecked(True)
        rButton_3P.toggled.connect(
            lambda: label_p3Type.setStyleSheet("color: #000000;"))
        rButton_3P.toggled.connect(
            lambda: cBox_p3.setDisabled(False))
        rButton_3P.toggled.connect(
            lambda: setItem(self.playerList, 2, 
            self.playerTypes[cBox_p3.currentText()]()))
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
        
        if not loaded:
            initialPlayerList = [HumanPlayer, Greedy1BotPlayer, Greedy2BotPlayer]
            for i in range(3):
                grid.addWidget(cBoxes[i], i+1, 2, 1, 2)
                cBoxes[i].addItems(list(self.playerTypes))
                cBoxes[i].setCurrentIndex(list(self.playerTypes.values()).index(initialPlayerList[i]))
            loaded = True
            del initialPlayerList

        cBox_p1.currentIndexChanged.connect(
            lambda: setItem(self.playerList, 0, self.playerTypes[cBox_p1.currentText()]()))
        # cBox_p1.currentIndexChanged.connect(
        #     lambda: print(self.playerList))
        cBox_p2.currentIndexChanged.connect(
            lambda: setItem(self.playerList, 1, self.playerTypes[cBox_p2.currentText()]()))
        # cBox_p2.currentIndexChanged.connect(
        #     lambda: print(self.playerList))
        cBox_p3.currentIndexChanged.connect(
            lambda: setItem(self.playerList, 2, self.playerTypes[cBox_p3.currentText()]()))
        # cBox_p3.currentIndexChanged.connect(
        #     lambda: print(self.playerList))
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
    
    #helpers for loadPlayerLoop and replayLoop
    def startGame(self):
        # print(self.playerList)
        self.loopNum = 2 #go to gameplay
        QtWidgets.QApplication.closeAllWindows()
    def backToMenu(self):
        self.loopNum = 0 #go to main menu
        QtWidgets.QApplication.closeAllWindows()
    def closing(self):
        if self.loopNum == 0 or self.loopNum == 1: self.backToMenu()
        elif self.loopNum == 2: self.startGame()
    def showNotValidReplay(self):
        print("This is not a valid replay!")
        self.loopNum = 0

    def mainMenuLoop(self, window:pygame.Surface):
        window.fill(WHITE)
        titleText = pygame.font.Font(size=int(WIDTH*0.08)).render(
            "Chinese Checkers", True, BLACK)
        titleTextRect = titleText.get_rect()
        titleTextRect.center = (WIDTH*0.5, HEIGHT*0.25)
        window.blit(titleText, titleTextRect)
        playButton = TextButton(
            "Play", centerx=int(WIDTH*0.5), centery=int(HEIGHT*0.375), width=WIDTH*0.25, height=HEIGHT*0.125, font_size=32)
        loadReplayButton = TextButton(
            "Load replay", centerx=int(WIDTH*0.5), centery=int(HEIGHT*0.625), width=WIDTH*0.25, height=HEIGHT*0.125, font_size=32)
        while True:
            ev = pygame.event.wait()
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()
            mouse_pos = pygame.mouse.get_pos()
            mouse_left_click = ev.type == MOUSEBUTTONDOWN
            if playButton.isClicked(mouse_pos, mouse_left_click):
                # print("play")
                self.loopNum = 1
                break
            if loadReplayButton.isClicked(mouse_pos, mouse_left_click):
                # print('load-replay')
                self.loopNum = 5
                break

            playButton.draw(window, mouse_pos)
            loadReplayButton.draw(window, mouse_pos)
            pygame.display.update()

def exactly_one_is_human(players: list[Player]):
    b = False
    for player in players:
        if b == False and isinstance(player, HumanPlayer):
            b = True
        elif b == True and isinstance(player, HumanPlayer):
            return False
    return b

def trainingLoop(g: Game, players: list[Player], recordReplay: bool=False):
    playingPlayerIndex = 0
    replayRecord = []
    if recordReplay:
        replayRecord.append(str(len(players)))
    for player in players:
        assert not isinstance(player, HumanPlayer), "Can't have humans during training! Human at player %d" % players.index(player) + 1
    for i in range(len(players)):
        players[i].setPlayerNum(i+1)
    while True:
        playingPlayer = players[playingPlayerIndex]
        start_coor, end_coor = playingPlayer.pickMove(g)
        g.movePiece(start_coor, end_coor)
        if recordReplay:
            replayRecord.append(str(start_coor)+' '+str(end_coor))
        winning = g.checkWin(playingPlayer.getPlayerNum())
        if winning and len(players) == 2:
            playingPlayer.has_won = True
            print('The winner is Player %d' % playingPlayer.getPlayerNum())
            print(f"{len(replayRecord)} moves")
            break #TODO: return stuff?
        elif winning and len(players) == 3:
            playingPlayer.has_won = True
            players.remove(playingPlayer)
            print("The first winner is Player %d" % playingPlayer.getPlayerNum())
        if playingPlayerIndex >= len(players) - 1: playingPlayerIndex = 0
        else: playingPlayerIndex += 1
