from game import Game, Field, GameEnded
from player import Player
from squares import *
from reader import read_field
from sys import exit

class Controller:
    def __init__(self, fname, chat_id):
        self.field = read_field(fname)
        self.chat_id = chat_id
        self.log("Начинается игра!")
        self.log("Поле имеет размеры {0}x{0}".format(self.field[0].size))
        self.log('Чтобы присоединиться, напишите мне в личку "го <имя> <начальная позиция>"')
        self.log("Английские буквы по горизонтали, цифры по вертикали")
        self.players = []
        self.pids = []
        while True:
            try:
                pid, action = self.receive().split()
                if action[0] == "старт":
                    break
                elif action[0] == "го":
                    self.add(pid, action[1], action[2])
            except Exception:
                pass

    def answer(self, pid, message):
        pass

    def receive(self, pid=None):
        pass

    def add(self, pid, name, pos):
        pos = None
        try:
            x = int(pos[1])
            y = ord(pos[0]) - ord('a')
            pos = (x, y)
            if not self.field[0].is_legal(pos):
                raise ValueError
        except ValueError:
            self.answer(pid, "Недопустимая позиция")
        else:
            self.players.append(Player(name, pos))
            self.pids.append(pid)
            self.answer(pid, "Отлично")

    def start(self):
        self.log("Игра начинается, если не знаете, что делать - пишите 'помощь'")
        self.game = Game(self, self.field, self.players)
        try:
            while True:
                pid, action = self.receive(self.pids[self.game.current_player])
                if pid != self.pids[self.game.current_player]:
                    continue
                if action == "помощь":
                    self.answer(self.pids[self.game.current_player], """
                    Возможные команды:
                    инвентарь - посмотреть инвентарь
                    в, н, л, п - сходить в заданную сторону
                    помощь - эта справка
                    <предмет> <действие> - использовать специальное действие предмета
                    """)
                self.game.action(action)
        except GameEnded:
            exit()

    def log(self, message):
        self.answer(self.chat_id, message)


class VkController(Controller):
    pass
