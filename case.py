"""
Class case who display dot in the board
"""
import pygame
from constant import DOT_COLOR, BOARD_COLOR, CASE_COLOR


class Case:
    def __init__(self, _screen, _number_or_dot, _pos_x, _pos_y):
        self.screen = _screen
        self.number_of_dot = _number_or_dot
        self.case_color = CASE_COLOR
        self.pos_x = _pos_x
        self.pos_y = _pos_y
        self.width = 140
        self.height = 100
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsans", 50)

    def generate_position(self):
        if self.number_of_dot < 10:
            x = self.pos_x + (self.width / 2 - 12)
            y = self.pos_y + (self.height / 2 - 35)
            return x, y
        elif self.number_of_dot >= 10:
            x = self.pos_x + (self.width / 2 - 25)
            y = self.pos_y + (self.height / 2 - 35)
            return x, y

    def draw(self):
        pygame.draw.rect(self.screen, self.case_color, self.rect)
        label = self.font.render(f"{self.number_of_dot}", 1, DOT_COLOR)
        pos_x_label, pos_y_label = self.generate_position()
        self.screen.blit(label, (pos_x_label, pos_y_label))

    def __repr__(self):
        return str(self.number_of_dot)
