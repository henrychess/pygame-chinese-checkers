from .game import *
from .player import *
from .helpers import *
import sys
import pygame
from pygame.locals import *
#import os
#import tkinter as tk
#from tkinter import filedialog
#import time

def exactly_one_is_human(players: list[Player]):
    b = False
    for player in players:
        if b == False and isinstance(player, HumanPlayer):
            b = True
        elif b == True and isinstance(player, HumanPlayer):
            return False
    return b

def gameplayLoop(g: Game, players: list[Player], window: pygame.Surface):
    playingPlayerIndex = 0
    humanPlayerNum = 0
    #returnStuff[0] is the winning player number
    #returnStuff[1] is replayRecord
    #if there are two players, len(returnStuff[0]) is 1
    #otherwise, it is 2, with the first winner at index 0
    returnStuff = [[],[]]
    replayRecord = []
    #replayRecord[0] marks the number of players
    replayRecord.append(str(len(players)))
    if exactly_one_is_human(players):
        for player in players:
            if isinstance(player, HumanPlayer):
                humanPlayerNum = player.getPlayerNum()
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
        replayRecord.append(str(start_coor)+' '+str(end_coor))
        winning = g.checkWin(playingPlayer.getPlayerNum())
        if winning and len(players) == 2:
            if humanPlayerNum != 0:
                g.drawBoard(window, humanPlayerNum)
            else: 
                g.drawBoard(window)
            playingPlayer.has_won = True
            returnStuff[0].append(playingPlayer.getPlayerNum())
            #TODO: show the message on screen
            print('The winner is Player %d' % playingPlayer.getPlayerNum())
            returnStuff[1] = replayRecord
            #pygame.quit(); sys.exit()
            return returnStuff
        elif winning and len(players) == 3:
            playingPlayer.has_won = True
            returnStuff[0].append(playingPlayer.getPlayerNum())
            players.remove(playingPlayer)
            #TODO: show the message on screen
            print("The first winner is Player %d" % playingPlayer.getPlayerNum())
        if playingPlayerIndex >= len(players) - 1: playingPlayerIndex = 0
        else: playingPlayerIndex += 1

def trainingLoop(g: Game, players: list[Player], recordReplay: bool=False):
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

def replayLoop(window: pygame.Surface):
    pass #TODO

def gameOverLoop(window: pygame.Surface, winnerList: list, replayRecord: list):
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
            return 1
        if exportReplayButton.isClicked(mouse_pos, mouse_left_click):
            with open("./replays/replay.txt", mode="w+") as f:
                for i in replayRecord:
                    f.write(str(i)+'\n')
            exportReplayButton.text = "Replay exported!"
            exportReplayButton.enabled = False
        menuButton.draw(window, mouse_pos, mouse_left_click)
        exportReplayButton.draw(window, mouse_pos, mouse_left_click)
        pygame.display.update()

def loadPlayerLoop(window: pygame.Surface):
    window.fill(WHITE)
    #do_stuff
    pygame.display.update()

def mainMenuLoop(window:pygame.Surface):
    window.fill(WHITE)
    playButton = TextButton("Play", 350, 200, 150, 70)
    loadReplayButton = TextButton("Load replay", 350, 400, 150, 70)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        mouse_pos = pygame.mouse.get_pos()
        mouse_left_click = pygame.mouse.get_pressed()[0]
        if playButton.isClicked(mouse_pos, mouse_left_click):
            print("play") #TODO: loadPlayerLoop
        if loadReplayButton.isClicked(mouse_pos, mouse_left_click):
            print('test')
            #'''
            file_path = prompt_file()
            if not file_path:
                print('file path is empty')
            else:
                print(file_path)
            #'''

        playButton.draw(window, mouse_pos, mouse_left_click)
        loadReplayButton.draw(window, mouse_pos, mouse_left_click)
        pygame.display.update()