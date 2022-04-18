import random

# класс логики игры
class PekingOpera:
    # конструктор получает кол-во строк, кол-во столбцов, кол-во ходов
    def __init__(self, row: int, col: int, moves: int):
        super(PekingOpera, self).__init__()
        self.row = row
        self.col = col
        self.best_score = 0
        self.moves = moves
        self.field_init()

    # инициализация поля
    def field_init(self):
        self.field = []
        for row in range(self.row):
            self.field.append([int(random.randint(1, 5)) for i in range(self.col)])
        self.score = 0
        self.check_combinations()
        self.pos = []
        self.score = 0
        self.moves_left = self.moves
        self.flag_change = False
        self.playing = True

    # добавление тех ячеек на которые нажимаешь
    def add_cell(self, row: int, col: int):
        self.pos.append([row, col])

        if len(self.pos) == 2:
            r1, c1 = self.pos[0][0], self.pos[0][1]
            r2, c2 = self.pos[1][0], self.pos[1][1]

            if (abs(r1 - r2) == 1 and abs(c1 - c2) == 0) or (abs(r1 - r2) == 0 and abs(c1 - c2) == 1):
                self.field[r1][c1], self.field[r2][c2] = self.field[r2][c2], self.field[r1][c1]
                self.check_combinations()
                if self.flag_change:
                    self.moves_left -= 1
                else:
                    self.field[r1][c1], self.field[r2][c2] = self.field[r2][c2], self.field[r1][c1]

            self.pos.clear()

        if self.moves_left == 0:
            self.playing = False

        if self.score > self.best_score:
            self.best_score = self.score

    # проверка ячеек на удаление
    def check_combinations(self):
        self.flag_change = False

        while 1 > 0:

            delete_cell = self.find_position()
            if len(delete_cell) != 0:
                for i in range(len(delete_cell)):
                    self.field[delete_cell[i][0]][delete_cell[i][1]] = 0
                    self.score += 1
                delete_cell.clear()
                self.reshuffle()
                self.flag_change = True
            else:
                break

    # поиск ячеек для удаления
    def find_position(self):
        delete_pos = []
        for i in range(self.row):
            temp = []
            temp.append([i, 0])
            for j in range(1, self.col):
                if self.field[i][j] == self.field[temp[0][0]][temp[0][1]]:
                    temp.append([i, j])
                else:
                    if len(temp) > 2:
                        for t in range(len(temp)):
                            delete_pos.append(temp[t])
                    temp.clear()
                    temp.append([i, j])
            if len(temp) > 2:
                for t in range(len(temp)):
                    delete_pos.append(temp[t])

        for i in range(self.col):
            temp = []
            temp.append([0, i])
            for j in range(1, self.row):
                if self.field[j][i] == self.field[temp[0][0]][temp[0][1]]:
                    temp.append([j, i])
                else:
                    if len(temp) > 2:
                        for t in range(len(temp)):
                            delete_pos.append(temp[t])
                    temp.clear()
                    temp.append([j, i])
            if len(temp) > 2:
                for t in range(len(temp)):
                    delete_pos.append(temp[t])

        return delete_pos

    # падение ячеек вниз
    def reshuffle(self):
        for i in range(self.row-1, 0, -1):
            for j in range(self.col):
                if self.field[i][j] == 0:
                    index = self.find_pos(i, j)
                    self.field[i][j], self.field[index][j] = self.field[index][j], self.field[i][j]

        for i in range(self.row):
            for j in range(self.col):
                if self.field[i][j] == 0:
                    self.field[i][j] = random.randint(1, 5)

    # поиск не пустой ячейки сверху
    def find_pos(self, i, j):
        row = i
        while row >= 0:
            if self.field[row][j] != 0:
                return row
            row -= 1
        return i-1

    def reset_game(self):
        self.field_init()
