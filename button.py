import pygame
from constant import BOARD_COLOR


class Button:
    def __init__(self, _screen, _pos_x, _pos_y, _label,_action):
        self.screen = _screen
        self.pos_x = _pos_x
        self.pos_y = _pos_y
        self.width = 140
        self.height = 28
        self.label = _label
        self.font = pygame.font.SysFont("comicsans", 25)
        self.action = _action

    def draw(self):
        pygame.draw.rect(self.screen, BOARD_COLOR, (self.pos_x, self.pos_y, self.width, self.height))
        _l = self.font.render(self.label, 1, (255, 255, 255))
        self.screen.blit(_l, (self.pos_x + self.width - len(self.label) * 20, self.pos_y + 5))

    def do(self):
        self.action()
