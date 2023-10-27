from game_logic.loops import *
from game_logic.game import *
from game_logic.player import *
import pygame, sys
from pygame.locals import *


pygame.init()
window = pygame.display.set_mode((800,600), pygame.SCALED | pygame.SRCALPHA)
pygame.display.set_caption('Chinese Checkers')

lc = LoopController()

while True:
    """ for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() """
    lc.mainLoop(window)
