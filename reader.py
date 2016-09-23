from collections import defaultdict
from squares import *
from game import Field
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

def read_field(fname):
    f = open(fname)
    subfield_number = int(f.readline())
    subfields = []
    for i in range(subfield_number):
        size = int(f.readline())
        field = [[None for i in range(size)] for j in range(size)]
        hwalls = [[None for i in range(size)] for j in range(size - 1)]
        vwalls = [[None for i in range(size - 1)] for j in range(size)]
        keys = defaultdict(lambda: [])
        for x in range(size):
            row = f.readline()
            for y in range(size):
                symbol = row[2 * y]
                if symbol == ".":
                    field[x][y] = Square()
                else:
                    keys[symbol].append((x, y))
                if y != size - 1:
                    vwalls[x][y] = row[2 * y + 1] == "|"
            if x != size - 1:
                row = f.readline()
                for y in range(size):
                    hwalls[x][y] = row[2 * y] == "-"
        for j in range(len(keys)):
            row = f.readline()
            symbol = row[0]
            print(symbol, keys[symbol], eval(row[1:]))
            for pos in keys[symbol]:
                field[pos[0]][pos[1]] = eval(row[1:])
        subfields.append(Field(size, field, vwalls=vwalls, hwalls=hwalls))
    return subfields
