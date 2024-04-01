import pygame
from colorsys import rgb_to_hls, hls_to_rgb
from game_logic.layout import DIRECTIONS
from game_logic.game import Game
from game_logic.helpers import add, abs_coors, h2c, mult, obj_to_subj_coor
from game_logic.piece import Piece
from gui.constants import (
    BLACK,
    GRAY,
    ORANGE,
    RED,
    WHITE,
    YELLOW,
    GREEN,
    PLAYER_COLORS,
    PURPLE,
    WIDTH,
    PLAYER_LABELS,
)


def highlightMove(g: Game, window: pygame.Surface, move):
    """
    Highlights the start and end coordinates of a move.
    """
    if move == []:
        return
    # Highlight start coordinate
    pygame.draw.circle(
        window,
        PURPLE,
        abs_coors(g.centerCoor, move[0], g.unitLength),
        g.circleRadius,
        g.lineWidth + 2,
    )

    # Highlight end coordinate
    pygame.draw.circle(
        window,
        PURPLE,
        abs_coors(g.centerCoor, move[1], g.unitLength),
        g.circleRadius,
        g.lineWidth + 2,
    )


def adjust_color_brightness(rgbTuple: tuple, factor):
    r, g, b = rgbTuple[0], rgbTuple[1], rgbTuple[2]
    h, l, s = rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    l = max(min(l * factor, 1.0), 0.0)
    r, g, b = hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def brighten_color(rgbTuple: tuple, factor=0.25):
    """To darken, use a negative value for factor.\n
    Factor is float with absolute value between 0 and 1, representing percentage."""
    return adjust_color_brightness(rgbTuple, 1 + factor)


def drawPath(g: Game, window: pygame.Surface, path: list):
    """
    Draws dots in the cells along the path of a move.
    """
    if path is None:
        return
    for i in range(len(path) - 1):
        cell = abs_coors(g.centerCoor, path[i], g.unitLength)
        nextCell = abs_coors(g.centerCoor, path[i + 1], g.unitLength)
        pygame.draw.circle(window, PURPLE, cell, int(0.3 * g.circleRadius))
        pygame.draw.circle(window, PURPLE, nextCell, int(0.3 * g.circleRadius))


def drawBoard(g: Game, window: pygame.Surface, playerNum: int = 1):
    """
    Draws the board polygon, lines and circles.
    """
    drawPolygons(g, window)
    drawTriangles(g, window, playerNum)
    drawLines(g, window)
    drawCircles(g, window, playerNum)
    # drawCoordinates(g, window)
    drawPlayerTypes(g, window)
    drawTurnCount(g, window)


def drawTurnCount(g: Game, window: pygame.Surface):
    """
    Adds the turn count to the window.
    """
    playerName = g.playerNames[g.playerNum - 1]
    n_players = len(g.playerNames)
    turn_cycle = (g.turnCount - 1) // n_players + 1
    subturn = (g.turnCount - 1) % n_players + 1
    text = pygame.font.Font(size=int(WIDTH * 0.04)).render(
        f"Turn: {turn_cycle}.{subturn}, {playerName}",
        True,
        BLACK,
        None,
    )
    textRect = text.get_rect()
    textRect.center = add(
        g.centerCoor,
        mult(h2c((-3, -7)), g.unitLength),
    )
    window.blit(text, textRect)


def drawPlayerTypes(g: Game, window: pygame.Surface):
    """
    Adds the player types to the window.
    """

    for p, coor in zip(g.playerList, PLAYER_LABELS):
        c = add(
            g.centerCoor,
            mult(h2c(coor), g.unitLength),
        )  # absolute coordinates on screen
        playerStr = type(p).__name__
        text = pygame.font.Font(size=int(WIDTH * 0.035)).render(
            playerStr,
            True,
            PLAYER_COLORS[p.getPlayerNum() - 1],
            None,
        )
        textRect = text.get_rect()
        textRect.center = c
        window.blit(text, textRect)


def drawCircles(g: Game, window: pygame.Surface, playerNum: int):
    for obj_coor in g.board:
        # Draw an empty cell
        coor = obj_to_subj_coor(obj_coor, playerNum, g.layout)
        c = add(
            g.centerCoor,
            mult(h2c(coor), g.unitLength),
        )  # absolute coordinates on screen
        pygame.draw.circle(window, WHITE, c, g.circleRadius)
        pygame.draw.circle(window, BLACK, c, g.circleRadius, g.lineWidth)

        # Draw player's piece if the cell is occupied
        if isinstance(g.board[obj_coor], Piece):
            pygame.draw.circle(
                window,
                PLAYER_COLORS[g.board[obj_coor].getPlayerNum() - 1],
                c,
                g.circleRadius - 2,
            )


def drawLines(g: Game, window: pygame.Surface):
    """
    Draws the black lines to connect the cells.
    """
    visited = set()
    neighbors = set()
    for coor in g.board:
        for dir in DIRECTIONS:
            n_coor = add(coor, dir)
            if n_coor not in visited and n_coor in g.board:
                neighbors.add(n_coor)
        for n_coor in neighbors:
            c = add(g.centerCoor, mult(h2c(coor), g.unitLength))
            n = add(g.centerCoor, mult(h2c(n_coor), g.unitLength))
            pygame.draw.line(window, BLACK, c, n, g.lineWidth)
        neighbors.clear()


def drawPolygons(g: Game, window: pygame.Surface):
    # center hexagon
    pygame.draw.polygon(
        window,
        GRAY,
        (
            abs_coors(g.centerCoor, (-4, 4), g.unitLength),
            abs_coors(g.centerCoor, (0, 4), g.unitLength),
            abs_coors(g.centerCoor, (4, 0), g.unitLength),
            abs_coors(g.centerCoor, (4, -4), g.unitLength),
            abs_coors(g.centerCoor, (0, -4), g.unitLength),
            abs_coors(g.centerCoor, (-4, 0), g.unitLength),
        ),
    )


def drawTriangles(g: Game, window: pygame.Surface, playerNum: int = 1):
    # Set sequence of player colours.
    if playerNum == 1:
        colors = (YELLOW, RED, GREEN)
    elif playerNum == 2:
        colors = (RED, GREEN, YELLOW)
    elif playerNum == 3:
        colors = (GREEN, YELLOW, RED)

    # Draw the 6 triangles
    pygame.draw.polygon(
        window,
        colors[0],
        (
            add(g.centerCoor, mult(h2c((-4, 8)), g.unitLength)),
            add(g.centerCoor, mult(h2c((-4, 4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((0, 4)), g.unitLength)),
        ),
    )
    pygame.draw.polygon(
        window,
        colors[0],
        (
            add(g.centerCoor, mult(h2c((0, -4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((4, -4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((4, -8)), g.unitLength)),
        ),
    )
    pygame.draw.polygon(
        window,
        colors[2],
        (
            add(g.centerCoor, mult(h2c((-4, 0)), g.unitLength)),
            add(g.centerCoor, mult(h2c((-4, -4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((0, -4)), g.unitLength)),
        ),
    )
    pygame.draw.polygon(
        window,
        colors[2],
        (
            add(g.centerCoor, mult(h2c((0, 4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((4, 4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((4, 0)), g.unitLength)),
        ),
    )
    pygame.draw.polygon(
        window,
        colors[1],
        (
            add(g.centerCoor, mult(h2c((4, 0)), g.unitLength)),
            add(g.centerCoor, mult(h2c((8, -4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((4, -4)), g.unitLength)),
        ),
    )
    pygame.draw.polygon(
        window,
        colors[1],
        (
            add(g.centerCoor, mult(h2c((-8, 4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((-4, 4)), g.unitLength)),
            add(g.centerCoor, mult(h2c((-4, 0)), g.unitLength)),
        ),
    )


def drawCoordinates(g: Game, window: pygame.Surface):
    """
    Adds the coordinates of each cell to the window.
    """
    for coor in g.board:
        c = add(
            g.centerCoor,
            mult(h2c(coor), g.unitLength),
        )  # absolute coordinates on screen
        coor_str = f"{coor[0]}, {coor[1]}"
        text = pygame.font.Font(size=int(WIDTH * 0.0175)).render(
            coor_str,
            True,
            BLACK,
            None,
        )
        textRect = text.get_rect()
        textRect.center = c
        window.blit(text, textRect)


class Button:
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        centerx: int = 0,
        centery: int = 0,
        width: int = 200,
        height: int = 100,
        enabled: bool = True,
        button_color: tuple = ORANGE,
    ) -> None:
        """self.x=x; self.y=y; self.width = width; self.height = height"""
        self.enabled = enabled
        self.button_color = button_color
        if centerx and centery:
            self.buttonRect = pygame.Rect(
                centerx - width / 2,
                centery - height / 2,
                width,
                height,
            )
        else:
            self.buttonRect = pygame.Rect(x, y, width, height)

    def draw(self, window: pygame.Surface, mouse_pos):
        if self.enabled:
            if self.isHovering(mouse_pos) and self.enabled:
                pygame.draw.rect(
                    window,
                    brighten_color(self.button_color, 0.25),
                    self.buttonRect,
                    0,
                    5,
                )
            else:
                pygame.draw.rect(
                    window,
                    self.button_color,
                    self.buttonRect,
                    0,
                    5,
                )
            pygame.draw.rect(window, BLACK, self.buttonRect, 2, 5)
        else:
            pygame.draw.rect(window, GRAY, self.buttonRect, 0, 5)

    def isClicked(self, mouse_pos, mouse_left_click):
        if (
            mouse_left_click
            and self.buttonRect.collidepoint(mouse_pos)
            and self.enabled
        ):
            return True
        else:
            return False

    def isHovering(self, mouse_pos):
        if self.buttonRect.collidepoint(mouse_pos):
            return True
        else:
            return False


class TextButton(Button):
    def __init__(
        self,
        text: str,
        x: int = 0,
        y: int = 0,
        centerx: int = 0,
        centery: int = 0,
        width: int = 200,
        height: int = 100,
        enabled: bool = True,
        font=None,
        font_size=16,
        text_color: tuple = BLACK,
        button_color: tuple = ORANGE,
    ):
        # super().__init__()
        self.enabled = enabled
        self.button_color = button_color
        if centerx and centery:
            self.buttonRect = pygame.Rect(
                centerx - width / 2,
                centery - height / 2,
                width,
                height,
            )
        else:
            self.buttonRect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color

    def draw(self, window: pygame.Surface, mouse_pos):
        """
        Fades the button if the mouse is hovering over it.
        """
        text = pygame.font.SysFont(self.font, self.font_size).render(
            self.text,
            True,
            self.text_color,
        )
        textRect = text.get_rect()
        textRect.center = self.buttonRect.center
        # color = self.button_color
        if not self.enabled:
            color = GRAY
        else:
            color = self.button_color
        pygame.draw.rect(window, color, self.buttonRect, 0, 5)
        if self.isHovering(mouse_pos) and self.enabled:
            pygame.draw.rect(
                window,
                brighten_color(color, 0.25),
                self.buttonRect,
                0,
                5,
            )
        pygame.draw.rect(window, BLACK, self.buttonRect, 2, 5)
        window.blit(text, textRect)
