game_field = [['\\', 1, 2, 3],
              [1, '-', '-', '-'],
              [2, '-', '-', '-'],
              [3, '-', '-', '-']]
rows = 4
cols = 4


def display_field(game_field):
    for i in range(rows):
        for j in range(cols):
            print(game_field[i][j], end=" ")
        print()


def request_coords(game_field, value):
    while True:
        c = input("Введите координаты через пробел: ").split(' ')
        i = int(c[0])
        if len(c) < 2:
            print('Не корректные координаты, повторите ввод')
            continue
        j = int(c[1])
        if game_field[i][j] == '-':
            game_field[i][j] = value
            break
        else:
            print('Ячейка занята, повторите ввод')


def win(f):
    if (f[1][1] == f[2][2] == f[3][3] or f[3][1] == f[2][2] == f[1][3]) and (f[2][2] == 'X' or f[2][2] == 'O'):
        return True
    for e in range(1, 4):
        if f[e][1] == f[e][2] == f[e][3] and (f[e][1] == 'X' or f[e][1] == 'O'):
            return True
    for e in range(1, 4):
        if f[1][e] == f[2][e] == f[3][e] and (f[1][e] == 'X' or f[1][e] == 'O'):
            return True
    return False


display_field(game_field)
player = 'O'
for move in range(9):
    print(f"Игрок {player} ваш ход!")
    request_coords(game_field, player)
    display_field(game_field)
    if win(game_field):
        print(f'Игрок {player} победил!')
        break
    if player == 'O':
        player = 'X'
    else:
        player = 'O'
