from constants import DIRECTIONS

class Object:
    "Это обычный предмет"
    pass

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
    "в/н/л/п - выстрелить в заданую сторону"
    @staticmethod
    def action(game, player, action):
        if action in DIRECTIONS:
            position = player.position
            direction = DIRECTIONS[action]
            while True:
                killed = False
                for other in game.players:
                    if other.position == position and other.field == player.field and player.name != other.name:
                        game.log("Вы попали в игрока {}".format(other.name))
                        other.die(game)
                        killed = True
                if killed:
                    return True
                if game.field.can_move(position, direction):
                    position = (position[0] + direction[0],
                            position[1] + direction[1])
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

@register_object("дубина")
class Club(Object):
    "в/н/л/п - ударить в заданую сторону"
    @staticmethod
    def action(game, player, action):
        if action in DIRECTIONS:
            hit = False 
            direction = DIRECTIONS[action]
            for other in game.players:
                if other.field == player.field and player.name != other.name and (other.position == player.position
                        or other.position == (player.position[0] + direction[0], player.position[1] + direction[1])):
                    game.log("Вы попали игроку {} прямо по голове".format(other.name))
                    hit = True
                    if game.fields[other.field].can_move(other.position, direction):
                        other.position = (other.position[0] + direction[0], other.position[1] + direction[1])
                        game.fields[other.field].squares[other.position[0]][other.position[1]].arrive(game, other) 
            if hit == False:
                game.log("Дубина со свистом рассекла воздух")
            return False
                        
