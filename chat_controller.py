from game import Game, Field, GameEnded
from player import Player
from squares import *
from reader import read_field
from sys import exit
import requests
import json
import vk
from collections import deque
from random import randint
from time import sleep

class Controller:
    def __init__(self, fname, chat_id):
        self.field = read_field(fname)
        self.chat_id = chat_id

    def answer(self, pid, message):
        raise NotImplementedError()

    def receive(self, pid=None):
        raise NotImplementedError()

    def log(self, message):
        raise NotImplementedError()

    def add(self, pid, name, pos):
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
        self.log("Начинается игра!")
        self.log("Поле имеет размеры {0}x{0}".format(self.field[0].size))
        self.log('Чтобы присоединиться, напишите мне в личку "го <имя> <начальная позиция>"')
        self.log("Английские буквы по горизонтали, цифры по вертикали")
        self.players = []
        self.pids = []
        while True:
            try:
                pid, action = self.receive()
                action = action.split()
                if action[0] == "старт":
                    break
                elif action[0] == "го":
                    self.add(pid, action[1], action[2])
            except IndexError:
                pass
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



class VkController(Controller):
    def __init__(self, fname, chat_id):
        session = vk.Session(access_token="")
        self.api = vk.API(session)
        self.messages = deque()
        self.data = None
        super(VkController, self).__init__(fname, chat_id)

    def get_messages(self):
        reps = None
        print("Try")
        while True:
            if not self.data:
                self.data = self.api.messages.getLongPollServer()
            resp = requests.api.get("https://{server}?act=a_check&key={key}&ts={ts}&wait=25&mode=2".format(**self.data))
            resp = json.loads(resp.content.decode('utf-8'))
            if "failed" not in resp:
                break
            self.data = None
        self.data["ts"] = resp["ts"]
        print(resp)
        print("Got {} updates".format(len(resp["updates"])))
        for el in resp["updates"]:
            if el[0] == 4:
                pid = el[3]
                if pid > 2000000000:
                    pid = el[7]['from']
                print("Got {} {}".format(pid, el[6]))
                self.messages.append((pid, el[6]))

    def receive(self, pid=None):
        print("Want from {}".format(pid))
        buf = []
        message = None
        while not message:
            while self.messages:
                message = self.messages.popleft()
                if pid and message[0] != pid:
                    buf.append(message)
                    message = None
                else:
                    break
            else:
                self.get_messages()
        for el in buf:
            self.messages.append(buf)
        print("Found {}".format(message))
        return message

    def send(self, message, **param):
        while True:
            try:
                self.api.messages.send(message="{} {}".format(randint(1, 1000), message), **param)
            except vk.exceptions.VkAPIError as e:
                sleep(5)
            else:
                break
        sleep(0.5)

    def answer(self, pid, message):
        self.send(message, user_id=pid)

    def log(self, message):
        self.send(message, chat_id=self.chat_id)
