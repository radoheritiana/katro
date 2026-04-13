"""
Class case who display dot in the board
"""
import pygame
import os
from constant import *


class Case:
    _bille_surface = None
    _bille_mask = None
    _animation_clock = None

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
        if Case._bille_surface is None:
            Case._bille_surface = pygame.image.load(os.path.join("assets", "bille.png")).convert_alpha()
            Case._bille_mask = pygame.mask.from_surface(Case._bille_surface)
        self.bille = Case._bille_surface
        self.mask = Case._bille_mask
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        if Case._animation_clock is None:
            Case._animation_clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsans", 50)

    def generate_position(self):
        if self.number_of_dot == 0:
            return []
        return [(self.pos_x + p[0], self.pos_y + p[1]) for p in POSITION[self.number_of_dot]]

    def draw(self):
        if not self.is_transition:
            pygame.draw.ellipse(self.screen, self.color, self.rect, self.line_weight)
        positions = self.generate_position()
        for position in positions:
            self.screen.blit(self.bille, (position[0], position[1], 24, 24))

    def translate(self, pos_x_final, pos_y_final, _redraw_fen, _should_continue=None):
        if not self.is_transition:
            return True

        while self.pos_x != pos_x_final or self.pos_y != pos_y_final:
            if _should_continue is not None and not _should_continue():
                return False
            pygame.event.pump()
            Case._animation_clock.tick(ANIMATION_FPS)

            if self.pos_x < pos_x_final:
                self.pos_x = min(self.pos_x + ANIMATION_STEP, pos_x_final)
            elif self.pos_x > pos_x_final:
                self.pos_x = max(self.pos_x - ANIMATION_STEP, pos_x_final)

            if self.pos_y < pos_y_final:
                self.pos_y = min(self.pos_y + ANIMATION_STEP, pos_y_final)
            elif self.pos_y > pos_y_final:
                self.pos_y = max(self.pos_y - ANIMATION_STEP, pos_y_final)

            self.draw()
            _redraw_fen()

        return True

    def __repr__(self):
        return str(self.number_of_dot)
