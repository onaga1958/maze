DIRECTIONS = {"вверх": (-1, 0), "вниз": (1, 0), "влево": (0, -1), "вправо": (0, 1)}

class GameEnded(Exception):
    pass

class Field:
    def __init__(self, size, squares, vwalls, hwalls):
        self.size = size
        self.squares = squares
        self.vert_walls = vwalls
        self.hor_walls = hwalls

    def is_legal(self, position):
        return 0 <= position[0] < self.size and 0 <= position[1] < self.size

    def can_move(self, position, direction):
        if not self.is_legal((position[0] + direction[0], position[1] + direction[1])):
            return False
        elif direction[0] == 0:
            return not self.vert_walls[position[0]][position[1] + min(0, direction[1])]
        else:
            return not self.hor_walls[position[0] + min(0, direction[0])][position[1]]

    def __getitem__(self, index):
        return self.squares[index[0]][index[1]]


class Game:
    def __init__(self, controller, field, players):
        self.controller = controller
        self.field = field
        self.players = players
        self.current_player = 0

    def log(self, message):
        self.controller.log(message)

    def player(self):
        return self.players[self.current_player]

    def next_move(self):
        self.current_player = (self.current_player + 1) % len(self.players)
        self.player().event(self, "before_move")
        self.log("Ход игрока {}".format(self.player()))

    def action(self, action):
        done = False
        if action in DIRECTIONS:
            self.move(DIRECTIONS[action])
            done = True 
        elif action == "инвентарь":
            self.log("Содержимое сумки: {}".format(self.player().inventory))
        elif action.split()[0] in self.player().inventory:
            done = self.player().inventory.action(self, self, self.player(), action)
        else:
            self.controller.log("Невозможное действие")
        if done:
            self.player().event(self, "move")
            self.next_move()

    def move(self, direction):
        result = self.field[self.player().position].can_move(self, self.player(), direction) 
        if result is None:
            result = self.field.can_move(self.player().position, direction)
            if result:
                self.player().position = (self.player().position[0] + direction[0],
                                          self.player().position[1] + direction[1])
                self.field[self.player().position].arrive(self, self.player())
        if result:
            self.log("Вы сходили")
        else:
            self.log("Там стена")

    def win(self, player):
        if player.event(self, "win"):
            return
        self.log("Игра завершена")
        raise GameEnded()
