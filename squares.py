from inventory import Inventory

class Square:
    def __init__(self, message=None):
        self.loot = Inventory()
        self.message = message

    def can_move(self, game, player, direction):
        return None

    def arrive(self, game, player):
        if self.loot:
            game.log("Найдены предметы: {}".format(self.loot))
            player.inventory.update(self.loot)
            self.loot = Inventory()
        if self.message:
            game.log(self.message)

class EffectorSquare(Square):
    def __init__(self, message, effect_class):
        super(EffectorSquare, self).__init__(message)
        self.effect_class = effect_class

    def arrive(self, game, player):
        super(EffectorSquare, self).arrive(game, player)
        player.effects.append(self.effect_class())

class Exit(Square):
    def __init__(self, direction):
        super(Exit, self).__init__()
        self.direction = direction

    def can_move(self, game, player, direction):
        if direction == self.direction:
            if "сокровище" in player.inventory:
                game.log("Вы вышли из лабиринта. Победа!")
                game.win(player)
            else:
                game.log("Вы уперлись в закрытую дверь")
        return None

class RubberRoom(Square):
    def __init__(self, direction):
        super(RubberRoom, self).__init__()
        self.direction = direction

    def can_move(self, game, player, direction):
        if direction == self.direction:
            game.log("Вы вышли из резиновой комнаты")
            return None
        return True

def Stuff(objects):
    class tmp(Square):
        def __init__(self, message=None):
            self.message = message
            self.loot = Inventory(objects)
    return tmp

