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
    def __init__(self, effect_class, message=None):
        super(EffectorSquare, self).__init__(message)
        self.effect_class = effect_class

    def arrive(self, game, player):
        super(EffectorSquare, self).arrive(game, player)
        player.effects.append(self.effect_class())
        player.effects[-1].event(game, player, "start")

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

class Stuff(Square):
    def __init__(self, objects, message=None):
        self.message = message
        self.loot = Inventory(objects)

class Hole(Square):
    def __init__(self, target):
        super(Hole, self).__init__()
        self.target = target

    def arrive(self, game, player):
        super(Hole, self).arrive(game, player)
        game.log("Вы попали в ДЫРУ.")
        player.position = self.target

class Armory(Square):
    obj = "патрон"
    count = 3

    def arrive(self, game, player):
        super(Armory, self).arrive(game, player)
        while player.inventory.count(self.obj) < self.count:
            player.inventory.add(self.obj)
        game.log("Вы попали на слад - теперь у вас есть {}x{}".format(self.obj, self.count))
