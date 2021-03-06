#!/usr/bin/python3
"""
Regenerate test after protocol change
Usage: regenerate_test.py test_file
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game import Game, Field, GameEnded
from player import Player
from reader import read_field
from position import Position
from sys import argv, exit


class Controller:

    def __init__(self, test_file):
        self.test_file = open(test_file, "r")
        self.output = open("{}.new".format(test_file), "w")
        field_file = self.test_file.readline()[:-1]
        print(field_file, file=self.output)
        field = read_field(field_file)
        player_number = int(self.test_file.readline())
        print(player_number, file=self.output)
        players = []
        for i in range(player_number):
            line = self.test_file.readline()[:-1]
            players.append(Player(str(i), Position(*map(int, line.split()))))
            print(line, file=self.output)
        self.game = Game(self, field, players)

    def loop(self):
        try:
            while True:
                action = self.test_file.readline()[:-1]
                if action[:3] != ">>>":
                    print("Expected action got {}".format(action))
                    exit(1)
                print(action, file=self.output)
                action = action[3:]
                self.game.action(action)
        except GameEnded:
            pass
        print("Successfuly regenerated!")
        self.output.close()

    def log(self, message):
        answer = self.test_file.readline()[:-1]
        print(message, file=self.output)


if __name__ == "__main__":
    if len(argv) < 1:
        print("Invalid number of arguments.")
        exit(1)
    test_file = argv[1]
    Controller(test_file).loop()
