
class MinMax:
    def __init__(self, player_one_dots, player_two_dots):
        self.current_player_one_dots = player_one_dots
        self.current_player_two_dots = player_two_dots
        self.test_player_one_dots = []
        self.test_player_two_dots = []

    def maximum_rate(self):
        rates = []
        for i in range(0, 8):
            print(self.current_player_one_dots)
            self.test_player_one_dots = self.current_player_one_dots
            self.test_player_two_dots = self.current_player_two_dots

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


if __name__ == "__main__":
    p1_dots = [2, 2, 2, 2, 2, 2, 2, 2]
    p2_dots = [2, 2, 2, 2, 2, 2, 2, 2]
    minmax = MinMax(p1_dots, p2_dots)
    rates = minmax.maximum_rate()
    print(len(rates))
    print(rates)
