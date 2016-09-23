from squares import *
from game import Field
NAMES = {"0": Square, "E": Exit, "T": Stuff({"сокровище": 1})}
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

def read_field(fname):
    f = open(fname)
    size = int(f.readline())
    field = [[None for i in range(size)] for j in range(size)]
    hwalls = [[None for i in range(size)] for j in range(size - 1)]
    vwalls = [[None for i in range(size - 1)] for j in range(size)]
    for x in range(size):
        row = f.readline()
        for y in range(size):
            field[x][y] = NAMES[row[2 * y]]
            if y != size - 1:
                vwalls[x][y] = row[2 * y + 1] == "|"
        if x != size - 1:
            row = f.readline()
            for y in range(size):
                hwalls[x][y] = row[2 * y] == "-"
    while True:
        row = f.readline()
        if not row:
            break
        row = row.split(":")
        x, y = map(int, row[:2])
        field[x][y] = field[x][y](*[eval(el) for el in row[2:]])
    for x in range(size):
        for y in range(size):
            if isinstance(field[x][y], type):
                field[x][y] = field[x][y]()
    return Field(size, field, vwalls=vwalls, hwalls=hwalls)
