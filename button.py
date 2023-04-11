import pygame
from constant import BOARD_COLOR, BUTTON_HOVER_COLOR


class Button:
    def __init__(self, _screen, _pos_x, _pos_y, _label):
        self.screen = _screen
        self.pos_x = _pos_x
        self.pos_y = _pos_y
        self.width = 140
        self.height = 35
        self.label = _label
        self.font = pygame.font.SysFont("comicsans", 20)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
        self.bg_color = BOARD_COLOR

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        _l = self.font.render(self.label, 1, (255, 255, 255))
        self.screen.blit(_l, (self.pos_x + self.width - len(self.label) * 20, self.pos_y + 3))

    def listen_event(self, event, _action):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.bg_color = BUTTON_HOVER_COLOR
            else:
                self.bg_color = BOARD_COLOR
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                _action()
