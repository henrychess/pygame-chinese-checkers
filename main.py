from game_logic.loops import *
from game_logic.game import *
from game_logic.player import *
import pygame, sys
from pygame.locals import *

pygame.init()
window = pygame.display.set_mode((800,600), pygame.SCALED | pygame.SRCALPHA)
pygame.display.set_caption('Chinese Checkers')

#set up the game
g = Game(2)
players = [Greedy2BotPlayer(1), Greedy2BotPlayer(2)]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    mainMenuLoop(window)
    #winnerList, replayRecord = gameplayLoop(g, players, window)
    #a = gameOverLoop(window, winnerList, replayRecord)
    #if a == 1: mainMenuLoop(window)