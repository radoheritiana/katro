import pygame

from constant import *
from board import Board
from button import Button


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.board = Board(self.screen, 4, 4, self.redraw_fen)

    def redraw_fen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.board.draw()
        pygame.display.update()

    def draw_menu(self):
        title_font = pygame.font.SysFont("comicsans", 70)
        title_label = title_font.render("Katro game", 1, (255, 255, 255))
        self.screen.blit(title_label, (260, 160))
        button_play = Button(self.screen, 330, 230, "Play", None)
        button_about = Button(self.screen, 330, 280, "About", None)
        button_play.draw()
        button_about.draw()

    def play(self, clock):
        clock.tick(FPS)
        self.redraw_fen()
        for event in pygame.event.get():
            self.board.listen_event(event)

    def main(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_menu()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.play(clock)

        pygame.quit()
