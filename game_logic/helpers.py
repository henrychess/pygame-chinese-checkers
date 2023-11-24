from .literals import *
import math
import pygame
from colorsys import rgb_to_hls, hls_to_rgb

def add(a: tuple, b: tuple):
    '''Insert two tuples, return them added as if they were vectors.'''
    if len(a) != len(b): raise TypeError('tuples of different length')
    return tuple(a[i]+b[i] for i in range(len(a)))
def mult(a: tuple, n: int):
    '''Insert a tuple and an int, return them multiplied as if the tuple were a vector.'''
    return tuple(a[i]*n for i in range(len(a)))
def absValues(iterable):
    """Inputs an iterable with all ints. Returns a list of their absolute values."""
    return [abs[int(i)] for i in iterable]
def checkJump(moves: list, board: dict, destination: tuple, direction: tuple, playerNum: int):
    '''Recursively checks if you can jump further. Helper function of getValidMoves().
    \nInputs and outputs are in objective coordinates'''
    for dir in DIRECTIONS:
        jumpDir = mult(dir, 2)
        if dir == mult(direction, -1) or add(destination, dir) not in board or add(destination, jumpDir) not in board or add(destination, jumpDir) in moves: continue
        elif board[add(destination, dir)] == None: continue
        else: dest = add(destination, jumpDir)
        if dest in moves: continue #prevents endless loops
        elif dest not in board or board[dest] != None: continue #out of bounds or two pieces in a line
        else: 
            moves.append(dest)
            try:
                checkJump(moves, board, dest, dir, playerNum) #recursively checks available squares
            except RecursionError:
                print("RecursionError from " + str(destination) + " to " + str(dest))

def setItem(listt, index, item):
    listt[index] = item

def obj_to_subj_coor(c: tuple, playerNum: int):
    p, q, r = c[0], c[1], 0-c[0]-c[1]
    if playerNum == 1 or playerNum not in (1,2,3): return c
    if playerNum == 2: return (r, p)
    if playerNum == 3: return (q, r)
def subj_to_obj_coor(c: tuple, playerNum: int):
    p, q, r = c[0], c[1], 0-c[0]-c[1]
    if playerNum == 1 or playerNum not in (1,2,3): return c
    if playerNum == 2: return (q, r)
    if playerNum == 3: return (r, p)
def sign_func(i: int):
    if i > 0: return 1
    if i < 0: return -1
    else: return 0
def distance(start: tuple, end: tuple):
    i = 0; c = start; p2 = end[0]; q2 = end[1]
    while c != end:
        p1 = c[0]; q1 = c[1]; dp = sign_func(p2 - p1); dq = sign_func(q2 - q1)
        if (dp == 1 and dq == 1) or (dp == -1 and dq == -1): dq = 0
        c = add(c, (dp, dq))
        i += 1
    return i
def rotate(coor: tuple, angleDegrees):
    x = coor[0]; y = coor[1]
    angle = math.radians(angleDegrees)
    return (math.cos(angle) * x - math.sin(angle) * y, math.sin(angle) * x + math.cos(angle) * y)
def h2c(coor: tuple):
    '''hexagonal to cartesian for pygame'''
    x = coor[0]; y = coor[1]
    x2 = x+0.5*y; y2 = -1 * 0.5 * (math.sqrt(3) * y)
    return(x2, y2)
def abs_coors(center:tuple, coor:tuple, unit:int):
    '''absolute coordinates on screen'''
    return add(center, mult(h2c(coor),unit))

def adjust_color_brightness(rgbTuple:tuple, factor):
    r, g, b = rgbTuple[0], rgbTuple[1], rgbTuple[2]
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)
def brighten_color(rgbTuple: tuple, factor=0.25):
    '''To darken, use a negative value for factor.\n
    Factor is float with absolute value between 0 and 1, representing percentage.'''
    return adjust_color_brightness(rgbTuple, 1 + factor)
def ints(s):
    l = [int(i) for i in s]
    if isinstance(s,tuple): return tuple(l)
    if isinstance(s, list): return l
    if isinstance(s, set): return set(l)

class Button:
    def __init__(self, x:int=0, y:int=0, centerx:int=0, centery:int=0, width:int=200, height:int=100, enabled:bool=True, button_color:tuple=ORANGE) -> None:
        """ self.x=x; self.y=y; self.width = width; self.height = height """
        self.enabled=enabled; self.button_color=button_color
        if centerx and centery:
            self.buttonRect = pygame.Rect(
                centerx - width / 2,
                centery - height / 2,
                width, height)
        else:
            self.buttonRect = pygame.Rect(x, y, width, height)
    
    def draw(self, window: pygame.Surface, mouse_pos):
        if self.enabled:
            if self.isHovering(mouse_pos) and self.enabled:
                pygame.draw.rect(window, brighten_color(self.button_color, 0.25), self.buttonRect, 0, 5)
            else: pygame.draw.rect(window, self.button_color, self.buttonRect, 0, 5)
            pygame.draw.rect(window, BLACK, self.buttonRect, 2, 5)
        else:
            pygame.draw.rect(window, GRAY, self.buttonRect, 0, 5)
        
    def isClicked(self, mouse_pos, mouse_left_click):
        if mouse_left_click and self.buttonRect.collidepoint(mouse_pos) and self.enabled:
            return True
        else: return False
    
    def isHovering(self, mouse_pos):
        if self.buttonRect.collidepoint(mouse_pos):
            return True
        else: return False

class TextButton(Button):
    def __init__(self, text: str, x:int=0, y:int=0, centerx:int=0, centery:int=0, width:int=200, height:int=100, enabled:bool=True, font=None, font_size=16, text_color:tuple=BLACK, button_color:tuple=ORANGE):
        #super().__init__()
        self.enabled=enabled; self.button_color=button_color
        if centerx and centery:
            self.buttonRect = pygame.Rect(
                centerx - width / 2,
                centery - height / 2,
                width, height)
        else:
            self.buttonRect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font; self.font_size = font_size; self.text_color = text_color; self.button_color = button_color
    
    def draw(self, window:pygame.Surface, mouse_pos):
        text = pygame.font.SysFont(self.font, self.font_size).render(self.text, True, self.text_color)
        textRect = text.get_rect()
        textRect.center = self.buttonRect.center
        #color = self.button_color
        if not self.enabled:
            color = GRAY
        else:
            color = self.button_color
        pygame.draw.rect(window, color, self.buttonRect, 0, 5)
        if self.isHovering(mouse_pos) and self.enabled:
            pygame.draw.rect(window, brighten_color(color, 0.25), self.buttonRect, 0, 5)
        pygame.draw.rect(window, BLACK, self.buttonRect, 2, 5)
        window.blit(text, textRect)

