from game_logic.loops import *
from game_logic.game import *
from game_logic.player import *
from game_logic.literals import *
import pygame

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.SRCALPHA)
pygame.display.set_caption('Chinese Checkers')

lc = LoopController()

while True:
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() """
    lc.mainLoop(window)
