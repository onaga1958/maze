from game import Game, Field, GameEnded
from player import Player
from squares import *
from reader import read_field

class Controller:
    def __init__(self):
        print("Введите имя файла с полем: ", end="")
        fname = input()
        field = read_field(fname)
        print("Введите имена игроков через пробел: ", end="")
        players = input().split()
        print("Введите позиции игроков в формате x:y через пробел: ", end="")
        positions = list(map(lambda x: tuple(map(int, x.split(":"))), input().split()))
        players = [Player(name, pos) for name, pos in zip(players, positions)]
        self.game = Game(self, field, players)

    def loop(self):
        try:
            while True:
                print("Введите команду: ", end="")
                action = input()
                self.game.action(action)
        except GameEnded:
            print("Игра завершилась")

    def log(self, message):
        print(message)



