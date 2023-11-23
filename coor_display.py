from game_logic.game import *
from game_logic.helpers import *
from game_logic.literals import *
import pygame

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
    if isinstance(g.board[obj_coor], Piece):
        pygame.draw.circle(window, PLAYER_COLORS[g.board[obj_coor].getPlayerNum()-1], c, g.circleRadius-2)
    coor_str = str(coor)
    text = pygame.font.Font(size=14).render(coor_str, True, BLACK, None)
    textRect = text.get_rect()
    textRect.center = c
    window.blit(text, textRect)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
