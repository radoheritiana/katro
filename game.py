import pygame

from constant import *
import time
from board import Board
from button import Button
from tkinter import messagebox


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen, 4, 4, self.redraw_fen)
        self.button_play = Button(self.screen, 330, 240, "Play")
        self.button_about = Button(self.screen, 330, 300, "About")

    def redraw_fen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.board.draw()
        pygame.display.update()

    def draw_menu(self):
        self.screen.fill(BACKGROUND_COLOR)
        title_font = pygame.font.SysFont("comicsans", 70)
        title_label = title_font.render("Katro game", 1, (255, 255, 255))
        self.screen.blit(title_label, (220, 120))
        self.button_play.draw()
        self.button_about.draw()

    def winning(self):
        current_p1_dots, current_p2_dots = self.board.get_current_number_of_dots()
        if current_p2_dots <= 1:
            return True, 1
        elif current_p1_dots <= 1:
            return True, 2
        return False, 0

    def main(self):
        running = True
        is_playing = False

        while running:
            if not is_playing:
                self.clock.tick(FPS)
                self.draw_menu()

            """is_winning, player = self.winning()
            if is_winning:
                p = ""
                if player == 1:
                    p = "IA"
                else:
                    p = "You"
                messagebox.askyesnocancel('Win', f"{p} win!!")
                is_playing = False
                running = False"""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    # button event
                    if self.button_play.rect.collidepoint(event.pos):
                        self.button_play.bg_color = BUTTON_HOVER_COLOR
                    else:
                        self.button_play.bg_color = BOARD_COLOR
                    if self.button_about.rect.collidepoint(event.pos):
                        self.button_about.bg_color = BUTTON_HOVER_COLOR
                    else:
                        self.button_about.bg_color = BOARD_COLOR
                    # board event
                    if is_playing:
                        """if self.board.current_move == 1:
                            for case in self.board.player_one_case:
                                if case.rect.collidepoint(event.pos):
                                    case.case_color = CASE_HOVER_COLOR
                                else:
                                    case.case_color = CASE_COLOR"""
                        if self.board.current_move == 2:
                            for case in self.board.player_two_case:
                                if case.rect.collidepoint(event.pos):
                                    case.case_color = CASE_HOVER_COLOR
                                else:
                                    case.case_color = CASE_COLOR
                        self.redraw_fen()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play.rect.collidepoint(event.pos):
                        is_playing = True
                        ia_start = messagebox.askquestion('Question', "Voulez vous que l'IA commence?")
                        self.redraw_fen()
                        if ia_start == "yes":
                            self.board.current_move = 1
                            time.sleep(1)
                            self.board.player_one_start()
                        else:
                            self.board.current_move = 2
                        self.redraw_fen()

                    if is_playing:
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

            pygame.display.update()

        pygame.quit()
