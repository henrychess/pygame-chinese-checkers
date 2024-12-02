import math
import sys
import pygame
from pygame import QUIT, MOUSEBUTTONDOWN
from game_logic.game import Game
from game_logic.player import Player
from game_logic.piece import Piece
from game_logic.helpers import ints
from gui.constants import (
    WIDTH,
    HEIGHT,
    WHITE,
    LIGHT_GRAY,
    PLAYER_COLORS,
    DARK_GRAY,
)
from gui.gui_helpers import (
    abs_coors,
    brighten_color,
    TextButton,
    obj_to_subj_coor,
    drawBoard,
)


class Human(Player):
    def __init__(self):
        super().__init__()

    def updatePieceColour(
        self,
        g: Game,
        window: pygame.Surface,
        mousePos: tuple,
        piece: Piece,
    ):
        """
        Brightens the color of the piece if the mouse is hovering over it.
        """
        coor = (
            obj_to_subj_coor(piece.getCoor(), self.playerNum, g.layout)
            if self.playerNum != 0
            else piece.getCoor()
        )
        absCoor = abs_coors(g.centerCoor, coor, g.unitLength)
        # Case 1: Mouse is hovering over piece, brighten its color
        if (
            math.dist(mousePos, absCoor) <= g.circleRadius
            and piece.mouse_hovering is False
        ):
            # Change the piece's color
            pygame.draw.circle(
                window,
                brighten_color(PLAYER_COLORS[piece.getPlayerNum() - 1], 0.75),
                absCoor,
                g.circleRadius - 2,
            )
            piece.mouse_hovering = True
        # Case 2: Mouse is not hovering over piece, return to original color
        elif (
            math.dist(mousePos, absCoor) > g.circleRadius
            and piece.mouse_hovering is True
            and tuple(window.get_at(ints(absCoor))) != WHITE
        ):
            pygame.draw.circle(
                window,
                PLAYER_COLORS[piece.getPlayerNum() - 1],
                absCoor,
                g.circleRadius - 2,
            )
            piece.mouse_hovering = False

    def pickMove(
        self,
        g: Game,
        window: pygame.Surface,
        humanPlayerNum: int = 0,
    ):
        """
        Returns the start and end coordinates of the selected move.
        """
        print(f"[Human] is player {self.playerNum}")
        pieceSet: set[Piece] = g.pieces[self.playerNum]
        validMoves = []
        clicking = False
        selected_piece_coor = ()
        prev_selected_piece_coor = ()
        while True:
            ev = pygame.event.wait()

            # Quit the game
            if ev.type == QUIT:
                pygame.quit()
                sys.exit()

            # Wait for a click. If mouse hovers on a piece, highlight it
            mousePos = pygame.mouse.get_pos()
            clicking = ev.type == MOUSEBUTTONDOWN

            # Return to main menu
            backButton = TextButton(
                "Back to Menu",
                width=int(HEIGHT * 0.25),
                height=int(HEIGHT * 0.0833),
                font_size=int(WIDTH * 0.04),
            )
            if backButton.isClicked(mousePos, clicking):
                return (False, False)

            backButton.draw(window, mousePos)

            for piece in pieceSet:
                coor = (
                    obj_to_subj_coor(piece.getCoor(), self.playerNum, g.layout)
                    if humanPlayerNum != 0
                    else piece.getCoor()
                )
                absCoor = abs_coors(g.centerCoor, coor, g.unitLength)

                # Update the color of the piece based on mouse hover position
                self.updatePieceColour(g, window, mousePos, piece)

                # If the selected piece is the current piece,
                # and there are valid moves,
                # draw a gray circle around the possible destinations.
                if selected_piece_coor == piece.getCoor() and validMoves != []:
                    for d in validMoves:
                        destCoor = (
                            abs_coors(
                                g.centerCoor,
                                obj_to_subj_coor(d, self.playerNum, g.layout),
                                g.unitLength,
                            )
                            if humanPlayerNum != 0
                            else abs_coors(g.centerCoor, d, g.unitLength)
                        )

                        # Gray circle if mouse is hovering over it
                        if math.dist(mousePos, destCoor) <= g.circleRadius:
                            if clicking:
                                move = [selected_piece_coor, d]
                                print(f"[Human] Move: {move}\n")
                                return [selected_piece_coor, d]
                            else:
                                pygame.draw.circle(
                                    window,
                                    LIGHT_GRAY,
                                    destCoor,
                                    g.circleRadius - 2,
                                )
                        # White circle if mouse is not hovering over it
                        else:
                            pygame.draw.circle(
                                window,
                                WHITE,
                                destCoor,
                                g.circleRadius - 2,
                            )

                # Check if the piece is selected
                if math.dist(mousePos, absCoor) <= g.circleRadius and clicking is True:
                    selected_piece_coor = piece.getCoor()
                    if (
                        prev_selected_piece_coor != ()
                        and selected_piece_coor != prev_selected_piece_coor
                    ):
                        if humanPlayerNum != 0:
                            drawBoard(g, window, self.playerNum)
                        else:
                            drawBoard(g, window)
                    prev_selected_piece_coor = selected_piece_coor

                    pygame.draw.circle(
                        window,
                        DARK_GRAY + (50,),
                        absCoor,
                        g.circleRadius,
                        g.lineWidth + 1,
                    )
                    validMoves = g.getValidMoves(
                        selected_piece_coor,
                        self.playerNum,
                    )

                # Draw gray circles around valid moves
                for c in validMoves:
                    c2 = (
                        obj_to_subj_coor(c, self.playerNum, g.layout)
                        if humanPlayerNum != 0
                        else c
                    )
                    pygame.draw.circle(
                        window,
                        DARK_GRAY,
                        abs_coors(g.centerCoor, c2, g.unitLength),
                        g.circleRadius,
                        g.lineWidth + 2,
                    )

            pygame.display.update()
