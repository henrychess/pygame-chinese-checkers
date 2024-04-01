import pygame
from gui.loops import LoopController
from gui.constants import WIDTH, HEIGHT

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.SRCALPHA)
pygame.display.set_caption("Chinese Checkers")


def main():
    # Initialize pygame window
    pygame.init()
    window = pygame.display.set_mode(
        (WIDTH, HEIGHT),
        pygame.SCALED | pygame.SRCALPHA,
    )
    pygame.display.set_caption("Chinese Checkers")

    waitBot = False  # True: bot waits for a key press before making a move
    layout = "TRIANGLE"  # "MIRROR" or "TRIANGLE"
    n_pieces = 15  # 10 or 15

    # Enter game control loop
    lc = LoopController(waitBot, layout, n_pieces)
    while True:
        lc.mainLoop(window)


if __name__ == "__main__":
    main()
