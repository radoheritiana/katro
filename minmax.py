
class MinMax:
    def __init__(self):
        self.current_player_one_dots = []
        self.current_player_two_dots = []
        self.test_player_one_dots = []
        self.test_player_two_dots = []

    def get_maximum_rate(self, p1_dots, p2_dots):
        self.current_player_one_dots = p1_dots
        self.current_player_two_dots = p2_dots
        max_rates = self.get_rates()
        max_rate = max_rates[0]
        for rate in max_rates:
            if rate['rate'] > max_rate['rate']:
                max_rate = rate
        return max_rate

    def get_rates(self):
        rates = []
        for i in range(0, 8):
            self.test_player_one_dots = self.current_player_one_dots.copy()
            self.test_player_two_dots = self.current_player_two_dots.copy()

            self.move(self.test_player_one_dots[i], i)
            rate = 0
            for dot in self.test_player_one_dots:
                rate += dot
            rates.append({"index": i, "rate": rate})

        return rates

    def first_row_blank(self):
        for i in range(4):
            if self.test_player_two_dots[i] > 0:
                return False

    def can_get_enemy_dot(self, index):
        if index in [4, 5, 6, 7]:
            return True

    def get_complementary_index(self, index):
        if self.first_row_blank():
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

    def move(self, case, _index):
        index = _index
        can_move = True
        while can_move:
            length = case
            self.test_player_one_dots[index] = 0
            for i in range(length):
                if index >= 7:
                    index = -1
                self.test_player_one_dots[index + 1] += 1
                index += 1

            if self.test_player_one_dots[index] != 1 and self.test_player_one_dots[index] != 0:
                if self.can_get_enemy_dot(index):
                    self.test_player_one_dots[index] += \
                        self.test_player_two_dots[self.get_complementary_index(index)]
                    self.test_player_two_dots[self.get_complementary_index(index)] = 0
                self.move(self.test_player_one_dots[index], index)
            can_move = False
