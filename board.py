import pygame
from constant import *
from case import Case
import time
from minmax import MinMax
from tkinter import messagebox
from stoppable_thread import StoppableThread

board_width = 170
board_height = 115


class Board:
    def __init__(self, _screen, _row, _col, redraw_fen) -> None:
        self.screen = _screen
        self.row = _row
        self.col = _col
        self.player_one_case = []
        self.player_two_case = []
        self.init_cases()
        self.current_move = 2
        self.redraw_fen = redraw_fen
        self.min_max = MinMax()
        self.player_one_total_dot, self.player_two_total_dot = self.get_current_number_of_dots()
        self.t1 = None
        self.t2 = None

    def init_cases(self):
        x_init = 45
        y_init = 35
        half = self.row / 2
        first_row_player_one = []
        second_row_player_one = []
        first_row_player_two = []
        second_row_player_two = []
        for i in range(1, self.row + 1):
            for j in range(1, self.col + 1):
                if i <= half:
                    case = Case(self.screen, 2, x_init, y_init)
                    if i == 1:
                        first_row_player_one.append(case)
                    elif i == 2:
                        second_row_player_one.append(case)
                else:
                    dy = 48
                    case = Case(self.screen, 2, x_init, y_init + dy)
                    if i == 3:
                        first_row_player_two.append(case)
                    elif i == 4:
                        second_row_player_two.append(case)
                x_init += CASE_WIDTH + 9
            x_init = 45
            y_init += CASE_HEIGHT + 5
        second_row_player_one.reverse()
        second_row_player_two.reverse()
        self.player_one_case = first_row_player_one + second_row_player_one
        self.player_two_case = first_row_player_two + second_row_player_two

    def listen_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            """if self.current_move == 1:
                for index, case in enumerate(self.player_one_case):
                    if case.rect.collidepoint(event.pos):
                        case.case_color = BLUE
                        self.player_one_move(case, index, self.redraw_fen)"""
            if self.current_move == 2:
                for index, case in enumerate(self.player_two_case):
                    if case.rect.collidepoint(event.pos):
                        case.case_color = BLUE
                        self.player_two_move(case, index, self.redraw_fen)
        elif event.type == pygame.MOUSEMOTION:
            """if self.current_move == 1:
                for case in self.player_one_case:
                    if case.rect.collidepoint(event.pos):
                        case.line_weight = 3
                        case.case_color = BLUE
                    else:
                        case.line_weight = 1
                        case.case_color = CASE_COLOR"""
            if self.current_move == 2:
                for case in self.player_two_case:
                    if case.rect.collidepoint(event.pos):
                        case.line_weight = 3
                        case.case_color = BLUE
                    else:
                        case.line_weight = 1
                        case.case_color = CASE_COLOR

    def player_one_move(self, case, index, _redraw_fen):
        player = 1
        if case.number_of_dot > 0:
            self.t1 = StoppableThread(name="move_one", target=self.move(case, index, player, _redraw_fen))
            self.t1.start()
            self.current_move = 2

    def player_two_move(self, case, index, _redraw_fen):
        player = 2
        if case.number_of_dot > 0:
            self.t2 = StoppableThread(name="move_two", target=self.move(case, index, player, _redraw_fen))
            self.t2.start()
            self.current_move = 1

    def first_row_blank(self, player):
        if player == 1:
            for i in range(4):
                if self.player_two_case[i].number_of_dot > 0:
                    return False
        elif player == 2:
            for i in range(4, 8):
                if self.player_one_case[i].number_of_dot > 0:
                    return False
        return True

    def can_get_enemy_dot(self, index, player):
        if player == 1:
            if index in [4, 5, 6, 7]:
                return True
        elif player == 2:
            if index in [0, 1, 2, 3]:
                return True
        return False

    def get_complementary_index(self, index, player):
        if player == 1:
            if self.first_row_blank(player):
                return index
            else:
                if index == 4:
                    return 3
                elif index == 5:
                    return 2
                elif index == 6:
                    return 1
                elif index == 7:
                    return 0
        elif player == 2:
            if self.first_row_blank(player):
                return index
            else:
                if index == 0:
                    return 7
                elif index == 1:
                    return 6
                elif index == 2:
                    return 5
                elif index == 3:
                    return 4

    def move(self, case, index, player, _redraw_fen):
        can_move = True
        while can_move:
            length = case.number_of_dot
            case.number_of_dot = 0
            for i in range(length):
                if index >= 7:
                    index = -1
                if player == 1:
                    self.player_one_case[index + 1].case_color = (0, 255, 255)
                    self.player_one_case[index + 1].number_of_dot += 1
                    self.redraw_fen()
                    time.sleep(0.4)
                    self.player_one_case[index + 1].case_color = CASE_COLOR
                    self.redraw_fen()
                elif player == 2:
                    self.player_two_case[index + 1].case_color = (0, 255, 255)
                    self.player_two_case[index + 1].number_of_dot += 1
                    self.redraw_fen()
                    time.sleep(0.4)
                    self.player_two_case[index + 1].case_color = CASE_COLOR
                    self.redraw_fen()
                index += 1
                _redraw_fen()

            if player == 1:
                if self.player_one_case[index].number_of_dot != 1 and self.player_one_case[index].number_of_dot != 0:
                    if self.can_get_enemy_dot(index, player):
                        self.player_one_case[index].number_of_dot += \
                            self.player_two_case[self.get_complementary_index(index, player)].number_of_dot
                        self.player_two_case[self.get_complementary_index(index, player)].number_of_dot = 0
                    # redraw fen
                    _redraw_fen()
                    # on verifie si le jeu est terminé
                    is_winning, p = self.winning()
                    if is_winning:
                        winner = ""
                        if p == 1:
                            winner = "IA"
                        elif p == 2:
                            winner = "You"
                        messagebox.showinfo("Win", f"{winner} win!!")
                        # on quitte le jeu
                        pygame.quit()
                        break
                    else:
                        self.player_one_total_dot, self.player_two_total_dot = self.get_current_number_of_dots()
                    self.move(self.player_one_case[index], index, player, _redraw_fen)
            elif player == 2:
                if self.player_two_case[index].number_of_dot != 1 and self.player_two_case[index].number_of_dot != 0:
                    if self.can_get_enemy_dot(index, player):
                        self.player_two_case[index].number_of_dot += \
                            self.player_one_case[self.get_complementary_index(index, player)].number_of_dot
                        self.player_one_case[self.get_complementary_index(index, player)].number_of_dot = 0
                    # redraw fen
                    _redraw_fen()
                    # on verifie si le jeu est terminé
                    is_winning, p = self.winning()
                    if is_winning:
                        winner = ""
                        if p == 1:
                            winner = "IA"
                        elif p == 2:
                            winner = "You"
                        messagebox.showinfo("Win", f"{winner} win!!")
                        pygame.quit()
                        break
                    else:
                        self.player_one_total_dot, self.player_two_total_dot = self.get_current_number_of_dots()
                    self.move(self.player_two_case[index], index, player, _redraw_fen)
            can_move = False

    def draw(self):
        # pygame.draw.rect(self.screen, BOARD_COLOR, (70, 50, 640, 239))
        # pygame.draw.rect(self.screen, CASE_COLOR, (70, 50, 640, 239), 1)
        # pygame.draw.rect(self.screen, BOARD_COLOR, (70, 291, 640, 239))
        # pygame.draw.rect(self.screen, CASE_COLOR, (70, 291, 640, 239), 1)
        # pygame.draw.rect(self.screen, CASE_COLOR, (340, 289, 100, 2))

        font = pygame.font.SysFont("comicsans", 20)
        score_player_one = font.render(f"IA : {self.player_one_total_dot}", True, (255, 255, 255))
        score_player_two = font.render(f"Player 2 : {self.player_two_total_dot}", True, (255, 255, 255))
        self.screen.blit(score_player_one, (370, 5))
        self.screen.blit(score_player_two, (340, 567))

        if self.current_move == 1:
            y_current_move = 30
        else:
            y_current_move = 320

        pygame.draw.rect(self.screen, BLUE, (10, y_current_move, 12, 239))

        for case in self.player_one_case:
            case.draw()
        for case in self.player_two_case:
            case.draw()

    def extract_dot_from_case(self):
        p1_dots = []
        p2_dots = []
        for case in self.player_one_case:
            p1_dots.append(case.number_of_dot)
        for case in self.player_two_case:
            p2_dots.append(case.number_of_dot)
        return p1_dots, p2_dots

    def player_one_start(self):
        time.sleep(2)
        p1_dots, p2_dots = self.extract_dot_from_case()
        max_rate = self.min_max.get_maximum_rate(p1_dots, p2_dots)
        self.player_one_move(self.player_one_case[max_rate['index']], max_rate['index'], self.redraw_fen)

    def player_one_turn(self):
        p1_dots, p2_dots = self.extract_dot_from_case()
        max_rate = self.min_max.get_maximum_rate(p1_dots, p2_dots)
        self.player_one_move(self.player_one_case[max_rate['index']], max_rate['index'], self.redraw_fen)

    def get_current_number_of_dots(self):
        p1_total = 0
        p2_total = 0
        for case in self.player_one_case:
            p1_total += case.number_of_dot
        for case in self.player_two_case:
            p2_total += case.number_of_dot
        return p1_total, p2_total

    def winning(self):
        p1_total, p2_total = self.get_current_number_of_dots()
        if p1_total <= 1:
            return True, 2
        if p2_total <= 1:
            return True, 1
        return False, 0
