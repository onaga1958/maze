from collections import defaultdict
from squares import *
from effects import *
from game import Subfield, Field
from position import Position
import importlib
from field import *
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

def read_field(fname):
    f = open(fname)
    subfield_number = int(f.readline())
    field = Field([])
    keys = defaultdict(lambda: [])
    for i in range(subfield_number):
        size = int(f.readline())
        squares = [[None for i in range(size)] for j in range(size)]
        hwalls = [[None for i in range(size)] for j in range(size - 1)]
        vwalls = [[None for i in range(size - 1)] for j in range(size)]
        for x in range(size):
            row = f.readline()
            for y in range(size):
                symbol = row[2 * y]
                if symbol in [".", " ", "O"]:
                    squares[x][y] = Square()
                else:
                    keys[symbol].append(Position(i, x, y))
                if y != size - 1:
                    vwalls[x][y] = row[2 * y + 1] == "|"
            if x != size - 1:
                row = f.readline()
                for y in range(size):
                    hwalls[x][y] = row[2 * y] == "="
        field.fields.append(Subfield(size, squares, vwalls=vwalls, hwalls=hwalls))
    for j in range(len(keys)):
        row = f.readline()
        symbol = row[0]
        for pos in keys[symbol]:
            print(pos.__dict__)
            field.fields[pos.field].squares[pos.x()][pos.y()] = eval(row[1:])
    return field
