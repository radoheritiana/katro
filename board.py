import pygame
import os
from constant import *
from case import Case
from minmax import MinMax
from tkinter import messagebox

board_width = 170
board_height = 115


class Board:
    def __init__(self, _screen, _row, _col, redraw_fen, _number_of_dots_per_case, sound_enabled=True, language="en") -> None:
        pygame.mixer.init()
        self.screen = _screen
        self.row = _row
        self.col = _col
        self.number_of_dots_per_case = _number_of_dots_per_case
        self.player_one_case = []
        self.player_two_case = []
        self.init_cases()
        self.current_move = 2
        self.redraw_fen = redraw_fen
        self.sound_enabled = sound_enabled
        self.language = language
        self.messages = {
            "en": {
                "quit_title": "Quit game",
                "quit_confirm": "Do you really want to end actual party?",
                "info_title": "Information",
                "lose": "You lose!",
                "win": "You win!",
            },
            "fr": {
                "quit_title": "Quitter la partie",
                "quit_confirm": "Voulez-vous vraiment quitter la partie ?",
                "info_title": "Information",
                "lose": "Vous avez perdu !",
                "win": "Vous avez gagne !",
            },
            "mga": {
                "quit_title": "Hivoaka amin'ny lalao",
                "quit_confirm": "Tena hivoaka amin'ity lalao ity ve ianao?",
                "info_title": "Fampahafantarana",
                "lose": "Resy ianao!",
                "win": "Nandresy ianao!",
            },
        }
        self.min_max = MinMax()
        self.player_one_total_dot, self.player_two_total_dot = self.get_current_number_of_dots()
        self.case_transition = None
        self.stop_requested = False
        self.impact_sound = pygame.mixer.Sound(os.path.join("assets", "son", "bois.ogg"))
        self.get_sound = pygame.mixer.Sound(os.path.join("assets", "son", "get.ogg"))
        self.win_sound = pygame.mixer.Sound(os.path.join("assets", "son", "win.ogg"))

    def _play_sound(self, sound):
        if self.sound_enabled:
            pygame.mixer.Sound.play(sound)

    def _poll_runtime_events(self):
        msg = self.messages.get(self.language, self.messages["en"])
        for event in pygame.event.get([pygame.QUIT]):
            if event.type == pygame.QUIT:
                if messagebox.askyesno(msg["quit_title"], msg["quit_confirm"]):
                    self.stop_requested = True
                    return False
        return True

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
                    case = Case(self.screen, self.number_of_dots_per_case, x_init, y_init)
                    if i == 1:
                        first_row_player_one.append(case)
                    elif i == 2:
                        second_row_player_one.append(case)
                else:
                    dy = 48
                    case = Case(self.screen, self.number_of_dots_per_case, x_init, y_init + dy)
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

    def player_one_move(self, case, index, _redraw_fen):
        player = 1
        if case.number_of_dot > 0:
            if not self.move(case, index, player, _redraw_fen):
                return False
            self.current_move = 2
        return True

    def player_two_move(self, case, index, _redraw_fen):
        player = 2
        if case.number_of_dot > 0:
            if not self.move(case, index, player, _redraw_fen):
                return False
            self.current_move = 1
        return True

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
            if index in [4, 5, 6, 7] and self.player_one_case[index].number_of_dot >= 1:
                return True
        elif player == 2:
            if index in [0, 1, 2, 3] and self.player_two_case[index].number_of_dot >= 1:
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
        active_cases = self.player_one_case if player == 1 else self.player_two_case
        opponent_cases = self.player_two_case if player == 1 else self.player_one_case

        while True:
            if not self._poll_runtime_events():
                return False
            length = case.number_of_dot
            case.number_of_dot = 0
            for i in range(length):
                if not self._poll_runtime_events():
                    return False
                number_of_dots_to_share = length - i
                if index >= 7:
                    index = -1

                # draw transition
                if not self.draw_transition(number_of_dots_to_share, index + 1, player):
                    return False
                self.redraw_fen()
                self._play_sound(self.impact_sound)
                active_cases[index + 1].number_of_dot += 1
                self.redraw_fen()
                index += 1
                _redraw_fen()

            # on verifie si le joueur peut prendre les pions de l'adversire
            if active_cases[index].number_of_dot <= 1:
                break

            if self.can_get_enemy_dot(index, player):
                complementary_index = self.get_complementary_index(index, player)
                to_add = opponent_cases[complementary_index].number_of_dot
                opponent_cases[complementary_index].number_of_dot = 0
                self._play_sound(self.get_sound)
                # draw get oponents dot
                if not self.draw_get_oponents_dots(to_add, index, complementary_index, player):
                    return False
                active_cases[index].number_of_dot += to_add

            # redraw fen
            _redraw_fen()
            # on verifie si le jeu est terminé
            is_winning, p = self.winning()
            if is_winning:
                msg = self.messages.get(self.language, self.messages["en"])
                message = ""
                if p == 1:
                    message = msg["lose"]
                elif p == 2:
                    message = msg["win"]
                self._play_sound(self.win_sound)
                messagebox.showinfo(msg["info_title"], message)
                pygame.quit()
                break

            self.player_one_total_dot, self.player_two_total_dot = self.get_current_number_of_dots()
            case = active_cases[index]

        return True

    def draw(self):
        font = pygame.font.SysFont("comicsans", 20)
        score_player_one = font.render(f"Player 1 : {self.player_one_total_dot}", True, (255, 255, 255))
        score_player_two = font.render(f"Player 2 : {self.player_two_total_dot}", True, (255, 255, 255))
        self.screen.blit(score_player_one, (345, 5))
        self.screen.blit(score_player_two, (345, 567))

        if self.current_move == 1:
            y_current_move = 30
        else:
            y_current_move = 320

        pygame.draw.rect(self.screen, BLUE, (10, y_current_move, 5, 240))

        for case in self.player_one_case:
            case.draw()
        for case in self.player_two_case:
            case.draw()

    def extract_dot_from_case(self):
        p1_dots = [case.number_of_dot for case in self.player_one_case]
        p2_dots = [case.number_of_dot for case in self.player_two_case]
        return p1_dots, p2_dots

    def decision(self, p1_dots, p2_dots):
        max_rate = self.min_max.get_maximum_rate(p1_dots, p2_dots)
        if max_rate['rate'] > 0:
            return max_rate
        else:
            p1_total, p2_total = self.get_current_number_of_dots()
            if p1_total > 2:
                index = 0
                _max = 0
                for i, d in enumerate(p1_dots):
                    if d > _max:
                        _max = d
                        index = i
                return {"index": index, "rate": 0}
            else:
                index = 0
                for i, d in enumerate(p1_dots):
                    if d > 0:
                        index = i
                return {"index": index, "rate": 0}

    def player_one_start(self):
        p1_dots, p2_dots = self.extract_dot_from_case()
        choice = self.decision(p1_dots, p2_dots)
        return self.player_one_move(self.player_one_case[choice['index']], choice['index'], self.redraw_fen)

    def player_one_turn(self):
        p1_dots, p2_dots = self.extract_dot_from_case()
        choice = self.decision(p1_dots, p2_dots)
        return self.player_one_move(self.player_one_case[choice['index']], choice['index'], self.redraw_fen)

    def get_current_number_of_dots(self):
        p1_total = sum(case.number_of_dot for case in self.player_one_case)
        p2_total = sum(case.number_of_dot for case in self.player_two_case)
        return p1_total, p2_total

    def winning(self):
        p1_total, p2_total = self.get_current_number_of_dots()
        if p1_total <= 1:
            return True, 2
        if p2_total <= 1:
            return True, 1
        return False, 0

    def draw_transition(self, _number_of_dots, _index, _player):
        pos_x_initial = None
        pos_y_initial = None
        pos_x_final = None
        pos_y_final = None
        index_prev = _index - 1
        # on redefinit index si plus petit que 0
        if index_prev == -1:
            index_prev = 7

        if index_prev in range(0, 7):
            if _player == 1:
                pos_x_initial, pos_y_initial = \
                    self.player_one_case[index_prev].pos_x, self.player_one_case[index_prev].pos_y
                pos_x_final, pos_y_final = self.player_one_case[_index].pos_x, self.player_one_case[_index].pos_y
            else:
                pos_x_initial, pos_y_initial = \
                    self.player_two_case[index_prev].pos_x, self.player_two_case[index_prev].pos_y
                pos_x_final, pos_y_final = self.player_two_case[_index].pos_x, self.player_two_case[_index].pos_y

        elif index_prev == 7:
            if _player == 1:
                pos_x_initial, pos_y_initial = \
                    self.player_one_case[index_prev].pos_x, self.player_one_case[index_prev].pos_y
                pos_x_final, pos_y_final = self.player_one_case[0].pos_x, self.player_one_case[_index].pos_y
            else:
                pos_x_initial, pos_y_initial = \
                    self.player_two_case[index_prev].pos_x, self.player_two_case[index_prev].pos_y
                pos_x_final, pos_y_final = self.player_two_case[0].pos_x, self.player_two_case[_index].pos_y

        self.case_transition = Case(self.screen, _number_of_dots, pos_x_initial, pos_y_initial)
        self.case_transition.is_transition = True
        return self.case_transition.translate(pos_x_final, pos_y_final, self.redraw_fen, self._poll_runtime_events)

    def draw_get_oponents_dots(self, to_add, index, complementary_index, player):
        if player == 1:
            pos_x_initial = self.player_two_case[complementary_index].pos_x
            pos_y_initial = self.player_two_case[complementary_index].pos_y
            pos_x_final = self.player_one_case[index].pos_x
            pos_y_final = self.player_one_case[index].pos_y
        else:
            pos_x_initial = self.player_one_case[complementary_index].pos_x
            pos_y_initial = self.player_one_case[complementary_index].pos_y
            pos_x_final = self.player_two_case[index].pos_x
            pos_y_final = self.player_two_case[index].pos_y

        self.case_transition = Case(self.screen, to_add, pos_x_initial, pos_y_initial)
        self.case_transition.is_transition = True
        return self.case_transition.translate(pos_x_final, pos_y_final, self.redraw_fen, self._poll_runtime_events)
