"""
Class case who display dot in the board
"""
import pygame
import os
from constant import *


class Case:
    def __init__(self, _screen, _number_or_dot, _pos_x, _pos_y):
        self.is_transition = False
        self.screen = _screen
        self.number_of_dot = _number_or_dot
        self.pos_x = _pos_x
        self.color = CASE_COLOR
        self.pos_y = _pos_y
        self.width = CASE_WIDTH
        self.height = CASE_HEIGHT
        self.line_weight = 1
        self.bille = pygame.image.load(os.path.join("assets", "bille.png"))
        self.mask = pygame.mask.from_surface(self.bille)
        self.bille.convert()
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsans", 50)

    def generate_position(self):
        positions = []
        if self.number_of_dot != 0:
            pos = POSITION[self.number_of_dot]
            for p in pos:
                x = self.pos_x + p[0]
                y = self.pos_y + p[1]
                positions.append((x, y))
        return positions

    def draw(self):
        if not self.is_transition:
            pygame.draw.ellipse(self.screen, self.color, self.rect, self.line_weight)
        positions = self.generate_position()
        for position in positions:
            self.screen.blit(self.bille, (position[0], position[1], 24, 24))

    def translate(self, pos_x_final, pos_y_final, _redraw_fen):
        dx = 3
        dy = 3
        # on verifie si les postions final sont inferieurs aux postions initial
        if self.pos_x >= pos_x_final and self.pos_y >= pos_y_final:
            dx = - 3
            dy = - 3
            # on effectue la translation
            if self.is_transition:
                while self.pos_x > pos_x_final or self.pos_y > pos_y_final:
                    if self.pos_x != pos_x_final:
                        self.pos_x += dx
                    if self.pos_y != pos_y_final:
                        self.pos_y += dy
                    self.draw()
                    _redraw_fen()
        elif self.pos_x >= pos_x_final and self.pos_y <= pos_y_final:
            dx = - 3
            # on effectue la translation
            if self.is_transition:
                while self.pos_x > pos_x_final or self.pos_y < pos_y_final:
                    if self.pos_x != pos_x_final:
                        self.pos_x += dx
                    if self.pos_y != pos_y_final:
                        self.pos_y += dy
                    self.draw()
                    _redraw_fen()
        elif self.pos_x <= pos_x_final and self.pos_y >= pos_y_final:
            dy = - 3
            # on effectue la translation
            if self.is_transition:
                while self.pos_x < pos_x_final or self.pos_y > pos_y_final:
                    if self.pos_x != pos_x_final:
                        self.pos_x += dx
                    if self.pos_y != pos_y_final:
                        self.pos_y += dy
                    self.draw()
                    _redraw_fen()
        elif self.pos_x <= pos_x_final and self.pos_y <= pos_y_final:
            # on effectue la translation
            if self.is_transition:
                while self.pos_x < pos_x_final or self.pos_y < pos_y_final:
                    if self.pos_x != pos_x_final:
                        self.pos_x += dx
                    if self.pos_y != pos_y_final:
                        self.pos_y += dy
                    self.draw()
                    _redraw_fen()

    def __repr__(self):
        return str(self.number_of_dot)
