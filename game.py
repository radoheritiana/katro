import pygame
import os
from constant import *
import time
from board import Board

BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "bg.jpg"))


class Game:
    def __init__(self, _start):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen, 4, 4, self.redraw_fen)
        self.board.current_move = _start

    def redraw_fen(self):
        BACKGROUND_IMAGE.convert()
        self.screen.blit(BACKGROUND_IMAGE, (0, 0, 800, 600))
        self.board.draw()
        pygame.display.update()

    def winning(self):
        current_p1_dots, current_p2_dots = self.board.get_current_number_of_dots()
        if current_p2_dots <= 1:
            return True, 1
        elif current_p1_dots <= 1:
            return True, 2
        return False, 0

    def main(self):
        running = True
        self.redraw_fen()

        if self.board.current_move == 1:
            self.board.player_one_start()

        while running:
            self.clock.tick(FPS)
            self.redraw_fen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    # board event
                    """if self.board.current_move == 1:
                        for case in self.board.player_one_case:
                            if case.rect.collidepoint(event.pos):
                                case.case_color = CASE_HOVER_COLOR
                            else:
                                case.case_color = CASE_COLOR"""
                    if self.board.current_move == 2:
                        for case in self.board.player_two_case:
                            if case.rect.collidepoint(event.pos):
                                case.case_color = BLUE
                            else:
                                case.case_color = CASE_COLOR
                    self.redraw_fen()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # board event
                    """if self.board.current_move == 1:
                        for index, case in enumerate(self.board.player_one_case):
                            if case.rect.collidepoint(event.pos):
                                case.case_color = CASE_COLOR
                                self.board.player_one_move(case, index, self.redraw_fen)"""
                    if self.board.current_move == 2:
                        for index, case in enumerate(self.board.player_two_case):
                            if case.rect.collidepoint(event.pos):
                                case.case_color = CASE_COLOR
                                self.board.player_two_move(case, index, self.redraw_fen)
                                time.sleep(1)
                                self.board.player_one_turn()
            if self.board.winning()[1]:
                break
            pygame.display.update()

        pygame.quit()
