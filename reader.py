from collections import defaultdict
from squares import *
from effects import *
from game import Field
import importlib
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

def read_field(fname):
    f = open(fname)
    try:
        importlib.import_module(fname.split(".")[0])
    except ImportError:
        pass
    subfield_number = int(f.readline())
    subfields = []
    keys = defaultdict(lambda: [])
    for i in range(subfield_number):
        size = int(f.readline())
        field = [[None for i in range(size)] for j in range(size)]
        hwalls = [[None for i in range(size)] for j in range(size - 1)]
        vwalls = [[None for i in range(size - 1)] for j in range(size)]
        for x in range(size):
            row = f.readline()
            for y in range(size):
                symbol = row[2 * y]
                if symbol in [".", " ", "O"]:
                    field[x][y] = Square()
                else:
                    keys[symbol].append((i, x, y))
                if y != size - 1:
                    vwalls[x][y] = row[2 * y + 1] == "|"
            if x != size - 1:
                row = f.readline()
                for y in range(size):
                    hwalls[x][y] = row[2 * y] == "-"
        subfields.append(Field(size, field, vwalls=vwalls, hwalls=hwalls))
    print(keys)
    for j in range(len(keys)):
        row = f.readline()
        symbol = row[0]
        print(symbol, keys[symbol])
        for pos in keys[symbol]:
            subfields[pos[0]].squares[pos[1]][pos[2]] = eval(row[1:])
    return subfields
