from constants import DIRECTIONS

class Object:
    def __init__(self, name):
        self.name = name
        self.count = 1

OBJECTS = {}

def register_object(name, cls=None):
    def helper(cls):
        OBJECTS[name] = cls
        return cls
    if cls is None:
        return helper
    else:
        return helper(cls)

register_object("сокровище", Object)

@register_object("патрон")
class Bullet(Object):
    @staticmethod
    def action(game, player, action):
        if action in DIRECTIONS:
            position = player.position
            direction = DIRECTIONS[action]
            while True:
                for other in game.players:
                    if other.position == position and player.name != other.name:
                        game.log("Вы попали в игрока {}".format(other.name))
                        other.die(game)
                        return True
                if game.field.can_move(position, direction):
                    position = (position[0] + direction[0],
                            position[1] + direction[1])
                else:
                    game.log("Вы промазали")
                    return True
