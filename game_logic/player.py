from .game import *
from .piece import *
from .literals import *
from .helpers import *
import random
import pygame
import math
from pygame.locals import *
import sys
import time

class Player:
    def __init__(self, playerNum: int):
        self.playerNum = playerNum
        self.has_won = False
    def getPlayerNum(self):
        return self.playerNum
    
    def pickMove(self, g:Game):
        #dummy function that should be overridden
        pass

class RandomBotPlayer(Player):
    def __init__(self, playerNum: int):
        super().__init__(playerNum)
    
    def pickMove(self, g: Game):
        '''returns [start_coor, end_coor]'''
        moves = g.allMovesDict(self.playerNum)
        l = []
        for coor in moves:
            if moves[coor] != []: l.append(coor)
        coor = random.choice(l)
        move = random.choice(moves[coor])
        return [subj_to_obj_coor(coor, self.playerNum), subj_to_obj_coor(move, self.playerNum)]

class GreedyRandomBotPlayer(Player):
    def __init__(self, playerNum: int):
        super().__init__(playerNum)
    
    def pickMove(self, g: Game):
        '''returns [start_coor, end_coor]'''
        moves = g.allMovesDict(self.playerNum)
        tempMoves = dict()
        #forward
        for coor in moves:
            if moves[coor] != []: tempMoves[coor] = []
            else: continue
            for dest in moves[coor]:
                if dest[1] > coor[1]: tempMoves[coor].append(dest)
        for coor in list(tempMoves):
            if tempMoves[coor] == []: del tempMoves[coor]
        if len(tempMoves) > 0:
            coor = random.choice(list(tempMoves))
            move = random.choice(tempMoves[coor])
        else:
            #sideways
            tempMoves.clear()
            for coor in moves:
                if moves[coor] != []: tempMoves[coor] = []
                else: continue
                for dest in moves[coor]:
                    if dest[1] == coor[1]: tempMoves[coor].append(dest)
            for coor in list(tempMoves):
                if tempMoves[coor] == []: del tempMoves[coor]
            coor = random.choice(list(tempMoves))
            move = random.choice(tempMoves[coor])
        return [subj_to_obj_coor(coor, self.playerNum), subj_to_obj_coor(move, self.playerNum)]

class Greedy1BotPlayer(Player):
    '''Always finds the move that moves a piece to the topmost square'''
    def __init__(self, playerNum: int):
        super().__init__(playerNum)

    def pickMove(self, g: Game):
        '''returns [start_coor, end_coor] in objective coordinates'''
        moves = g.allMovesDict(self.playerNum)
        #state = g.boardState(self.playerNum)
        forwardMoves = dict()
        sidewaysMoves = dict()
        start_coor = ()
        end_coor = ()
        #split moves into forward and sideways
        for coor in moves:
            if moves[coor] != []: forwardMoves[coor] = []; sidewaysMoves[coor] = []
            else: continue
            for dest in moves[coor]:
                if dest[1] > coor[1]: forwardMoves[coor].append(dest)
                if dest[1] == coor[1]: sidewaysMoves[coor].append(dest)
        for coor in list(forwardMoves):
            if forwardMoves[coor] == []: del forwardMoves[coor]
        for coor in list(sidewaysMoves):
            if sidewaysMoves[coor] == []: del sidewaysMoves[coor]
        
        #choose the furthest destination (biggest y value in dest),
        #then backmost piece (smallest y value in coor)
        biggestDestY = -8
        smallestStartY = 8
        if len(forwardMoves) == 0:
            start_coor = random.choice(list(sidewaysMoves))
            end_coor = random.choice(sidewaysMoves[start_coor])
        else:
            for coor in forwardMoves:
                for i in range(len(forwardMoves[coor])):
                    dest = forwardMoves[coor][i]
                    if dest[1] > biggestDestY:
                        start_coor = coor; end_coor = dest
                        biggestDestY = dest[1]
                        smallestStartY = coor[1]
                    elif dest[1] == biggestDestY:
                        startY = coor[1]
                        if startY < smallestStartY:
                            start_coor = coor; end_coor = dest
                            biggestDestY = dest[1]
                            smallestStartY = coor[1]
                        elif startY == smallestStartY:
                            start_coor, end_coor = random.choice([[start_coor, end_coor], [coor, dest]])
                            biggestDestY = end_coor[1]
                            smallestStartY = start_coor[1]
        return [subj_to_obj_coor(start_coor, self.playerNum), subj_to_obj_coor(end_coor, self.playerNum)]

class Greedy2BotPlayer(Player):
    '''Always finds a move that jumps through the maximum distance (dest[1] - coor[1])'''
    def __init__(self, playerNum: int):
        super().__init__(playerNum)

    def pickMove(self, g: Game):
        '''returns [start_coor, end_coor] in objective coordinates\n
        return [subj_to_obj_coor(start_coor, self.playerNum), subj_to_obj_coor(end_coor, self.playerNum)]'''
        moves = g.allMovesDict(self.playerNum)
        #state = g.boardState(self.playerNum)
        forwardMoves = dict()
        sidewaysMoves = dict()
        start_coor = ()
        end_coor = ()
        max_dist = 0
        #split moves into forward and sideways
        for coor in moves:
            if moves[coor] != []: forwardMoves[coor] = []; sidewaysMoves[coor] = []
            else: continue
            for dest in moves[coor]:
                if dest[1] > coor[1]: forwardMoves[coor].append(dest)
                if dest[1] == coor[1]: sidewaysMoves[coor].append(dest)
        for coor in list(forwardMoves):
            if forwardMoves[coor] == []: del forwardMoves[coor]
        for coor in list(sidewaysMoves):
            if sidewaysMoves[coor] == []: del sidewaysMoves[coor]
        #if forward is empty, move sideways
        if len(forwardMoves) == 0:
            start_coor = random.choice(list(sidewaysMoves))
            end_coor = random.choice(sidewaysMoves[start_coor])
            return [subj_to_obj_coor(start_coor, self.playerNum), subj_to_obj_coor(end_coor, self.playerNum)]
        #forward: max distance
        for coor in forwardMoves:
            for dest in forwardMoves[coor]:
                if start_coor == () and end_coor == ():
                    start_coor = coor; end_coor = dest
                    max_dist = end_coor[1] - start_coor[1]
                else:
                    dist = dest[1] - coor[1]
                    if dist > max_dist:
                        max_dist = dist; start_coor = coor; end_coor = dest
                    elif dist == max_dist:
                        #prefers to move the piece that is more backwards
                        if dest[1] < end_coor[1]: max_dist = dist; start_coor = coor; end_coor = dest
        return [subj_to_obj_coor(start_coor, self.playerNum), subj_to_obj_coor(end_coor, self.playerNum)]

class HumanPlayer(Player):
    def __init__(self, playerNum: int):
        super().__init__(playerNum)
    
    def pickMove(self, g:Game, window:pygame.Surface, humanPlayerNum: int=0):
        pieceSet:set[Piece] = g.pieces[self.playerNum]
        validmoves = []
        clicking = False
        selected_piece_coor = ()
        prev_selected_piece_coor = ()
        #pygame.event.set_allowed([QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP])
        while True:
            """ ev = pygame.event.wait()
            if ev == QUIT: sys.exit() """
            #pygame.time.Clock().tick(30)
            for ev in pygame.event.get():
                if ev == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                elif ev == MOUSEBUTTONDOWN:
                    clicking = True
                elif ev == MOUSEBUTTONUP:
                    clicking = False
            #wait for a click,
            #if mouse hovers on a piece, highlight it
            mouse_pos = pygame.mouse.get_pos()
            clicking = pygame.mouse.get_pressed()[0]
            #
            if g.screen_is_altered:
                g.drawBoard(window, self.playerNum)
                g.screen_is_altered = False
            #print(time.time())
            for piece in pieceSet:
                coor = obj_to_subj_coor(piece.getCoor(), self.playerNum) if humanPlayerNum != 0 else piece.getCoor()
                absCoor = abs_coors(g.centerCoor, coor, g.unitLength)
                if math.dist(mouse_pos, absCoor) <= g.circleRadius and piece.mouse_hovering == False:
                    #change the piece's color
                    pygame.draw.circle(window, brighten_color(PLAYER_COLORS[piece.getPlayerNum()-1], 0.75), absCoor, g.circleRadius-2)
                    piece.mouse_hovering = True
                elif math.dist(mouse_pos, absCoor) > g.circleRadius and piece.mouse_hovering == True and tuple(window.get_at(ints(absCoor))) != WHITE:
                    #draw a circle of the original color
                    pygame.draw.circle(window, PLAYER_COLORS[piece.getPlayerNum()-1], absCoor, g.circleRadius-2)
                    piece.mouse_hovering = False
                #when a piece is selected, and you click any of the valid destinations,
                #you will move that piece to the destination
                if selected_piece_coor == piece.getCoor() and validmoves != []:
                    for d in validmoves:
                        destCoor = abs_coors(g.centerCoor, obj_to_subj_coor(d, self.playerNum), g.unitLength) if humanPlayerNum != 0 else abs_coors(g.centerCoor, d, g.unitLength)
                        if math.dist(mouse_pos, destCoor) <= g.circleRadius:
                            if clicking:
                                return [selected_piece_coor, d]
                            #draw a gray circle
                            pygame.draw.circle(window, LIGHT_GRAY, destCoor, g.circleRadius-2)
                        elif math.dist(mouse_pos, destCoor) > g.circleRadius:
                            #draw a white circle
                            pygame.draw.circle(window, WHITE, destCoor, g.circleRadius-2)
                #clicking the piece
                if math.dist(mouse_pos, absCoor) <= g.circleRadius and clicking == True:
                    selected_piece_coor = piece.getCoor()
                    if prev_selected_piece_coor != () and selected_piece_coor != prev_selected_piece_coor:
                        if humanPlayerNum != 0: g.drawBoard(window, self.playerNum)
                        else: g.drawBoard(window)
                    prev_selected_piece_coor = selected_piece_coor
                    #draw a semi-transparent gray circle outside the piece
                    pygame.draw.circle(window, (161,166,196,50), absCoor, g.circleRadius, g.lineWidth+1)
                    #piece.selected = True
                    #draw semi-transparent circles around all coordinates in getValidMoves()
                    validmoves = g.getValidMoves(selected_piece_coor, self.playerNum)
                    for c in validmoves:
                        c2 = obj_to_subj_coor(c, self.playerNum) if humanPlayerNum != 0 else c
                        pygame.draw.circle(window, (161,166,196,50), abs_coors(g.centerCoor, c2, g.unitLength), g.circleRadius, g.lineWidth+1)

            pygame.display.update()
            #return [start_coor, end_coor]
