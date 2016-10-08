from constants import DIRECTIONS
from .common_object import Object, register_object


@register_object("патрон")
class Bullet(Object):
    "в/н/л/п - выстрелить в заданую сторону"
    @staticmethod
    def action(game, player, action):
        if action in DIRECTIONS:
            position = player.position
            direction = DIRECTIONS[action]
            while True:
                killed = False
                for other in game.players:
                    if other.position == position and player.name != other.name:
                        game.log("Вы попали в игрока {}".format(other.name))
                        other.die(game)
                        killed = True
                if killed:
                    return True
                if game.field.can_move(position, direction):
                    position += direction
                else:
                    game.log("Вы промазали")
                    return True

@register_object("скакалка")
class Jumping_Rope(Object):
    "прыгать - проверить: земля ли под Вами?"
    @staticmethod
    def action(game, player, action):
        if action == "прыгать":
            game.log("Вы попрыгали. Кажется, под Вами и правда земля")
            return False 
