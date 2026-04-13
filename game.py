import pygame
import os
from constant import *
from board import Board
from tkinter import messagebox

BACKGROUND_IMAGE = pygame.image.load(os.path.join("assets", "bg.jpg"))


class Game:
    def __init__(self, _start, _dots):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        icon = pygame.image.load(os.path.join("assets", "favicon.ico"))
        pygame.display.set_icon(icon)
        self.number_of_dots_per_case = _dots
        self.board = Board(self.screen, 4, 4, self.redraw_fen, self.number_of_dots_per_case)
        self.board.current_move = _start
        self.is_break = False
        self.bg_music = pygame.mixer.music.load(os.path.join("assets", "son", 'bg.ogg'))
        self.background = BACKGROUND_IMAGE.convert()
        self.ai_move_due_at_ms = None

    def redraw_fen(self):
        self.screen.blit(self.background, (0, 0, 800, 600))
        self.board.draw()
        if self.board.case_transition:
            self.board.case_transition.draw()
        pygame.display.update()

    def draw_fen(self):
        self.screen.blit(self.background, (0, 0, 800, 600))
        self.board.draw()
        if self.board.case_transition:
            self.board.case_transition.draw()
        pygame.display.update()

    def winning(self):
        current_p1_dots, current_p2_dots = self.board.get_current_number_of_dots()
        if current_p2_dots <= 1:
            return True, 1
        elif current_p1_dots <= 1:
            return True, 2
        return False, 0

    def main(self):
        pygame.mixer.music.play(-1)
        running = True
        self.redraw_fen()
        clock = pygame.time.Clock()

        if self.board.current_move == 1:
            self.ai_move_due_at_ms = pygame.time.get_ticks() + 500

        while running:
            clock.tick(FPS)
            redraw_needed = False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    if self.board.current_move == 2:
                        for case in self.board.player_two_case:
                            if case.rect.collidepoint(event.pos):
                                case.line_weight = 2
                                case.color = LIGHT_BLUE
                            elif not case.rect.collidepoint(event.pos):
                                case.line_weight = 1
                                case.color = CASE_COLOR
                        redraw_needed = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.board.current_move == 2:
                        for index, case in enumerate(self.board.player_two_case):
                            if case.rect.collidepoint(event.pos):
                                case.line_weight = 1
                                case.color = CASE_COLOR
                                self.board.player_two_move(case, index, self.redraw_fen)
                                self.ai_move_due_at_ms = pygame.time.get_ticks() + 500
                                redraw_needed = True
                                break
                elif event.type == pygame.QUIT:
                    if messagebox.askyesno("Quit game", "Do you really want to end actual party?"):
                        running = False
                        break

            if self.board.current_move == 1 and self.ai_move_due_at_ms is not None:
                if pygame.time.get_ticks() >= self.ai_move_due_at_ms:
                    self.ai_move_due_at_ms = None
                    self.board.player_one_turn()
                    redraw_needed = True

            if self.board.winning()[1]:
                break

            if redraw_needed:
                self.redraw_fen()
            pygame.display.update()
        pygame.quit()
