from inventory import Object, register_object
from constants import DIRECTIONS

register_object("сокровище", Object)

@register_object("патрон")
class Bullet(Object):
    def action(self, game, player, action):
        if action in DIRECTIONS:
            position = player.position
            direction = DIRECTIONS[action]
            while True:
                for other in game.players:
                    if other.position == position and player.name != other:
                        game.log("Вы попали в игрока {}".format(other.name))
                        other.die()
                        return True
                if game.field.can_move(position, direction):
                    position = (position[0] + direction[0],
                            position[1] + direction[1])
                else:
                    game.log("Вы промазали")
                    return True
