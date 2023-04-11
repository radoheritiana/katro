import pygame
from constant import *
from case import Case
import time
import threading


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

    def init_cases(self):
        x_init = 80
        y_init = 60
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
                    case = Case(self.screen, 2, x_init, y_init)
                    if i == 3:
                        first_row_player_two.append(case)
                    elif i == 4:
                        second_row_player_two.append(case)
                x_init += 140 + 20
            x_init = 80
            y_init += 110 + 10
        second_row_player_one.reverse()
        second_row_player_two.reverse()
        self.player_one_case = first_row_player_one + second_row_player_one
        self.player_two_case = first_row_player_two + second_row_player_two

    def listen_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_move == 1:
                for index, case in enumerate(self.player_one_case):
                    if case.rect.collidepoint(event.pos):
                        case.case_color = CASE_COLOR
                        self.player_one_move(case, index)
            elif self.current_move == 2:
                for index, case in enumerate(self.player_two_case):
                    if case.rect.collidepoint(event.pos):
                        case.case_color = CASE_COLOR
                        self.player_two_move(case, index)
        elif event.type == pygame.MOUSEMOTION:
            if self.current_move == 1:
                for case in self.player_one_case:
                    if case.rect.collidepoint(event.pos):
                        case.case_color = CASE_HOVER_COLOR
                    else:
                        case.case_color = CASE_COLOR
            elif self.current_move == 2:
                for case in self.player_two_case:
                    if case.rect.collidepoint(event.pos):
                        case.case_color = CASE_HOVER_COLOR
                    else:
                        case.case_color = CASE_COLOR

    def player_one_move(self, case, index, _redraw_fen):
        player = 1
        if case.number_of_dot > 0:
            t = threading.Thread(name="move", target=self.move(case, index, player, _redraw_fen))
            t.start()
            self.current_move = 2

    def player_two_move(self, case, index, _redraw_fen):
        player = 2
        if case.number_of_dot > 0:
            t = threading.Thread(name="move", target=self.move(case, index, player, _redraw_fen))
            t.start()
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
                    time.sleep(0.25)
                    self.player_one_case[index + 1].case_color = CASE_COLOR
                    self.redraw_fen()
                elif player == 2:
                    self.player_two_case[index + 1].case_color = (0, 255, 255)
                    self.player_two_case[index + 1].number_of_dot += 1
                    self.redraw_fen()
                    time.sleep(0.25)
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
                    self.move(self.player_one_case[index], index, player, _redraw_fen)
            elif player == 2:
                if self.player_two_case[index].number_of_dot != 1 and self.player_two_case[index].number_of_dot != 0:
                    if self.can_get_enemy_dot(index, player):
                        self.player_two_case[index].number_of_dot += \
                            self.player_one_case[self.get_complementary_index(index, player)].number_of_dot
                        self.player_one_case[self.get_complementary_index(index, player)].number_of_dot = 0
                    self.move(self.player_two_case[index], index, player, _redraw_fen)

            can_move = False

    def draw(self):
        pygame.draw.rect(self.screen, BOARD_COLOR, (70, 50, 640, 239))
        pygame.draw.rect(self.screen, CASE_COLOR, (70, 50, 640, 239), 1)
        pygame.draw.rect(self.screen, BOARD_COLOR, (70, 291, 640, 239))
        pygame.draw.rect(self.screen, CASE_COLOR, (70, 291, 640, 239), 1)
        pygame.draw.rect(self.screen, CASE_COLOR, (340, 289, 100, 2))

        player_one_dot = self.get_player_one_dots()
        player_two_dot = self.get_player_two_dots()
        font = pygame.font.SysFont("comicsans", 24)
        score_player_one = font.render(f"Player 1 : {player_one_dot}", 1, (255, 255, 255))
        score_player_two = font.render(f"Player 2 : {player_two_dot}", 1, (255, 255, 255))
        self.screen.blit(score_player_one, (330, 10))
        self.screen.blit(score_player_two, (330, 550))

        if self.current_move == 1:
            y_current_move = 50
        else:
            y_current_move = 291

        pygame.draw.rect(self.screen, BLUE, (55, y_current_move, 8, 239))

        for case in self.player_one_case:
            case.draw()
        for case in self.player_two_case:
            case.draw()

    def get_player_one_dots(self):
        total = 0
        for case in self.player_one_case:
            total += case.number_of_dot
        return total

    def get_player_two_dots(self):
        total = 0
        for case in self.player_two_case:
            total += case.number_of_dot
        return total
