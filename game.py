from constants import DIRECTIONS
from objects import OBJECTS
from emoji import emojize

class GameEnded(Exception):
    pass

class Subfield:
    def __init__(self, size, squares, vwalls, hwalls):
        self.size = size
        self.squares = squares
        self.vert_walls = vwalls
        self.hor_walls = hwalls

    def is_legal(self, position):
        return 0 <= position.x() < self.size and 0 <= position.y() < self.size

    def can_move(self, position, direction):
        if not self.is_legal(position + direction):
            return False
        elif direction[0] == 0:
            return not self.vert_walls[position.x()][position.y() + min(0, direction[1])]
        else:
            return not self.hor_walls[position.x() + min(0, direction[0])][position.y()]

    def _move(self, game, player, direction):
        player.position += direction
        self[player.position].arrive(game, player)

    def __getitem__(self, index):
        return self.squares[index.x()][index.y()]

class Field:
    def __init__(self, fields):
        self.fields = fields

    def is_legal(self, position):
        return (0 <= position.field < len(self.fields) and
                self.fields[position.field].is_legal(position))

    def _move(self, game, player, direction):
        self.fields[player.position.field]._move(game, player, direction)

    def can_move(self, position, direction):
        return self.fields[position.field].can_move(position, direction)

    def move(self, game, direction):
        NAME = {(0, 1): "вправо :arrow_right:", (0, -1): "влево :arrow_left:", (-1, 0): "вверх :arrow_up:", (1, 0): "вниз :arrow_down:"}
        result = self[game.player().position].can_move(game, game.player(), direction) 
        if result is None:
            result = self.can_move(game.player().position, direction)
            if result:
                self._move(game, game.player(), direction)
        if result:
            game.log(game.player(), emojize("Вы сходили {}".format(NAME[direction]), use_aliases=True))
        else:
            game.log(game.player(), emojize("Невозможно сходить {}. Там стена :no_entry:".format(NAME[direction]), use_aliases=True))

    def __getitem__(self, position):
        return self.fields[position.field][position]


class Game:
    def __init__(self, controller, field, players):
        self.controller = controller
        self.field = field
        self.players = players
        self.current_player = -1
        self.turn_number = 0
        self.next_move()

    def log(self, player, message=None):
        if message is None:
            message = player
        else:
            message = "{}: {}".format(player, message)
        self.controller.log(message)

    def player(self):
        return self.players[self.current_player]

    def next_move(self):
        while True:
            self.current_player = (self.current_player + 1) % len(self.players)
            if self.current_player == 0:
                for player in self.players:
                    player.event(self, "start_turn")
                self.turn_number += 1
                self.log("Начинается {} ход".format(self.turn_number))
            if self.player().active:
                break
        self.log("--- {} ---".format(self.player()))
        self.player().event(self, "before_move")

    def action(self, action):
        done = False
        if action in DIRECTIONS:
            self.field.move(self, DIRECTIONS[action])
            done = True 
        elif action.split()[0] == "помощь":
            action = action.split()
            if len(action) > 1:
                obj = action[1]
                if not obj in self.player().inventory:
                    self.log("У вас нет такого предмета")
                else:
                    self.log(OBJECTS[obj].__doc__)
            else:
                self.log("""
Возможные команды:
инвентарь - посмотреть инвентарь
в, н, л, п - сходить в заданную сторону
помощь - эта справка
помощь <предмет> - справка по предмету
<предмет> <действие> - использовать специальное действие предмета
                        """)
        elif action == "инвентарь":
            self.log("Содержимое сумки: {}".format(self.player().inventory))
        elif action.split()[0] in self.player().inventory:
            done = self.player().inventory.action(self, self.player(), action)
        if done:
            self.player().event(self, "move")
            self.next_move()

    def win(self, player):
        if player.event(self, "win"):
            return
        self.log("Игра завершена")
        raise GameEnded()
    
    def __getstate__(self):
        return (self.field, self.players, self.current_player)

    def __setstate__(self, state):
        self.field, self.players, self.current_player = state
