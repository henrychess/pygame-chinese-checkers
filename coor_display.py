from game_logic.game import *
from game_logic.helpers import *
from game_logic.literals import *
import pygame, sys

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('Chinese Checkers Coordinates')
g = Game(3)
window.fill(WHITE)
g.drawPolygons(window)
g.drawLines(window)
for coor in g.board:
    c = add(g.centerCoor, mult(h2c(coor),g.unitLength)) #absolute coordinates on screen
    pygame.draw.circle(window, WHITE, c, g.circleRadius)
    pygame.draw.circle(window, BLACK, c, g.circleRadius, g.lineWidth)
    if isinstance(g.board[coor], Piece):
        pygame.draw.circle(window, PLAYER_COLORS[g.board[coor].getPlayerNum()-1], c, g.circleRadius-2)
    coor_str = f"{coor[0]}, {coor[1]}"
    text = pygame.font.Font(size=int(WIDTH*0.0175)).render(coor_str, True, BLACK, None)
    textRect = text.get_rect()
    textRect.center = c
    window.blit(text, textRect)
pygame.display.update()
# pygame.image.save(window, "screenshot.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
