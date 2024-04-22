from random import randint, shuffle


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить во вне игрового поля"


class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту точку"


class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.y + 1}, {self.x + 1})"


class Ship:
    def __init__(self, head, l, o):
        self.head = head
        self.l = l
        self.o = o
        self.lives = l

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.l):
            cur_y = self.head.y
            cur_x = self.head.x

            if self.o == 0:  # Ориентация корабля вдоль оси "Х" (горизонтально)
                cur_x += i
            elif self.o == 1:  # Ориентация корабля вдоль оси "У" (вертикально)
                cur_y += i

            ship_dots.append(Dot(cur_y, cur_x))
        return ship_dots

    def hit(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.hid = hid
        self.size = size
        self.count = 0
        self.field = [[" ~ "] * size for _ in range(size)]
        self.busy = []
        self.ships = []
        self.lucky_shot = False
        self.lucky_coord = Dot(0, 0)

    def __str__(self):
        res = ""
        res += "\\ | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} |" + "|".join(row) + "|"

        if self.hid:
            res = res.replace("■", "~")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.y + dy, d.x + dx)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.y][cur.x] = " ¤ "
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.y][d.x] = " ■ "
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.hit(d):
                ship.lives -= 1
                self.lucky_shot = True
                self.lucky_coord = d
                self.field[d.y][d.x] = " X "
                if ship.lives == 0:
                    self.lucky_shot = False
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[d.y][d.x] = " T "
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        if self.enemy.lucky_shot:
            shifts = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            shuffle(shifts)
            count = 0
            for s in shifts:
                count += 1
                y = self.enemy.lucky_coord.y + s[0]
                x = self.enemy.lucky_coord.x + s[1]
                d = Dot(y, x)
                # print("   >>>ai shoots after luck<<<   ", self.enemy.lucky_coord, d)
                if y < 0 or x < 0 or y > (self.enemy.size - 1) or x > (self.enemy.size - 1):
                    # print(f">>> out of bounds {y} {x}")
                    continue
                if self.enemy.field[d.y][d.x] == " ¤ " or self.enemy.field[d.y][d.x] == " T " or self.enemy.field[d.y][d.x] == " X ":
                    # print(">>> mimos <<<")
                    continue
            if count >= 4:
                self.enemy.lucky_shot = False
            if count >= 4 and ((d.y < 0 or d.x < 0 or d.y > (self.enemy.size - 1) or d.x > (self.enemy.size - 1)) or
                               (self.enemy.field[d.y][d.x] == " ¤ " or self.enemy.field[d.y][d.x] == " T " or
                                self.enemy.field[d.y][d.x] == " X ")):
                d = self.random_coords()
        else:
            d = self.random_coords()
        print(f"Ход компьютера: {d.y + 1} {d.x + 1}")
        return d

    def random_coords(self):
        while True:
            y = randint(0, 5)
            x = randint(0, 5)
            d = Dot(y, x)
            if self.enemy.field[d.y][d.x] == " ¤ " or self.enemy.field[d.y][d.x] == " T " or self.enemy.field[d.y][d.x] == " X ":
                continue
            break
        return d


class User(Player):
    def ask(self):
        while True:
            coords = input("Ваш ход: ").split()

            if len(coords) != 2:
                print("Введите 2 координаты!")
                continue

            y, x = coords

            if not (y.isdigit()) or not (x.isdigit()):
                print("Введите числа!")

            y, x = int(y), int(x)
            return Dot(y - 1, x - 1)


class Game:
    def __init__(self, size=6):
        self.lens = [3, 2, 2, 1, 1, 1, 1]
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        # self.us = User(pl, co)
        self.us = AI(pl, co)

    def greet(self):
        print("-------------------------")
        print("     Приветствуем вас    ")
        print("        в игре           ")
        print("      морской бой        ")
        print("-------------------------")
        print("   Формат ввода:  Х  У   ")
        print("   Х - номер строки      ")
        print("   У - номер столбца     ")
        print("-------------------------")

    def try_board(self):
        board = Board(size=self.size)
        attempts = 0
        for l in self.lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass

        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def print_boards_horizontal(self):
        str = "  Доска пользователя         |   Доска компьютера        |\n"
        str += "\\ | 1 | 2 | 3 | 4 | 5 | 6 |  | \\ | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.us.board.field):
            str += f"\n{i + 1} |" + "|".join(row) + "|  |"
            s = f" {i + 1} |" + "|".join(self.ai.board.field[i]) + "|"
            if self.ai.board.hid:
                s = s.replace("■", "~")
            str += s
        print("-" * 58)
        print(str)
        print("-" * 58)

    def print_boards(self):
        print("-" * 20)
        print("Доска пользователя")
        print(self.us.board)
        print("-" * 20)
        print("Доска компьютера")
        print(self.ai.board)
        print("-" * 20)

    def loop(self):
        num = 0
        while True:
            # self.print_boards()
            self.print_boards_horizontal()
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_boards_horizontal()
                print("-" * 20)
                print("Пользователь выиграл")
                break

            if self.us.board.defeat():
                self.print_boards_horizontal()
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


if __name__ == "__main__":
    g = Game()
    g.start()
