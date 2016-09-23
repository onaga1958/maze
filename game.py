from constants import DIRECTIONS

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

    def move(self, game, direction):
        result = self[game.player().position].can_move(game, game.player(), direction) 
        if result is None:
            result = self.can_move(game.player().position, direction)
            if result:
                game.player().position = (game.player().position[0] + direction[0],
                        game.player().position[1] + direction[1])
                game.field[game.player().position].arrive(game, game.player())
        if result:
            game.log("Вы сходили")
        else:
            game.log("Там стена")

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
            self.field.move(self, DIRECTIONS[action])
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

    def win(self, player):
        if player.event(self, "win"):
            return
        self.log("Игра завершена")
        raise GameEnded()
