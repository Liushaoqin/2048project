import msvcrt
import os
from random import choice,randrange
keys = [i for i in 'wsadre']
instrument = ['Up', 'Down', 'Left', 'Right', 'Reset', 'Exit']
ins_dict = dict(zip(keys, instrument))

def trans(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

def get_key():
    c = 'N'
    while c not in keys:
        c = msvcrt.getch()
        if ord(c) < 128:
            c = c.decode()
    return ins_dict[c]

class Gamefield(object):
    def __init__(self, width=4, win=2048):
        self.score = 0
        self.width = width
        self.highscore = 0
        self.win = win
        self.reset()

    def reset(self):
        self.field = [[0 for i in range(self.width)] for j in range(self.width)]
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.get_num()
        self.get_num()
        self.draw()

    def move(self, direction):
        def move_left(row):
            def tighten(row):
                num = 0
                for i in range(self.width):
                    if row[i] != 0:
                        row[num] = row[i]
                        num+=1
                for i in range(num,self.width):
                    row[i] = 0
                return row

            def merge(row):
                for i in range(0,self.width-1):
                    if row[i] == row[i+1]:
                        row[i] = row[i]*2
                        if self.score < row[i]:
                            self.score = row[i]
                        row[i+1] = 0
                return row

            tighten(row)
            merge(row)
            tighten(row)
            return row

        moves = {}
        moves['Left'] = lambda field: [move_left(row) for row in field]
        moves['Right'] = lambda field:invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:trans(moves['Left'](trans(field)))
        moves['Down'] = lambda field:invert(trans(moves['Left'](invert(trans(field)))))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.get_num()
                return True
            return False

    def move_is_possible(self,direction):
        def move_left(row):
            for i in range(4 - 1):
                if row[i] == 0 and row[i+1] != 0:
                    return True
                if row[i] == row[i+1] and row[i] != 0:
                    return True
            return False

        moves = {}
        moves['Left'] = lambda field: any(move_left(row) for row in field)
        moves['Right'] = lambda field:moves['Left'](invert(field))
        moves['Up'] = lambda field: moves['Left'](trans(field))
        moves['Down'] = lambda field: moves['Left'](invert(trans(field)))
        if direction in moves:
            return moves[direction](self.field)
        return False

    def get_num(self):
        new_element = 4 if randrange(0,100)>89 else 2
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.width) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def is_win(self):
        return self.score >= self.win

    def draw(self):
        os.system('cls')
        for row in self.field:
            print(row)

if __name__ == '__main__':
    def init():
        gamefield.reset()
        return 'Game'

    def not_game(state):
        if state =='Win':
            os.system('cls')
            print("you Win!")
        if state == 'Gameover':
            os.system('cls')
            print("Game Over")
        op = get_key()
        if op == 'Exit':
            return 'Exit'
        else:
            return 'Init'

    def game():
        gamefield.draw()
        op = get_key()
        if op == 'Reset':
            return 'Init'
        elif op == 'Exit':
            return 'Exit'
        else:
            gamefield.move(op)
            if gamefield.is_win():
                return 'Win'
            else:
                return 'Game'

    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    # 设置终结状态最大数值为 32
    gamefield = Gamefield(win=32)
    state = 'Init'
    while state != 'Exit':
        state = state_actions[state]()



