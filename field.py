from squares import Square
from objects import register_object, Object
class Minotaur(Square):
    def arrive(self, game, player):
        game.log("Вы попались МИНОТАВРУ. Жуткий конец.")
        player.die(game)

@register_object("посох")
class Bullet(Object):
    "Это древний артефакт - Посох Несчастного Лурьехи. Кажется, если им 'махнуть', что-то произойдет"
    @staticmethod
    def action(game, player, action):
        if action == "махнуть":
            if not hasattr(player, 'cock'):
                game.log("Вы взмахнули посохом - и стены лабиринта огласил дурацкий смех.")
                player.name = "Петух {}".format(player.name)
                player.cock = True
            else:
                game.log('"Петух! Петух!" - раздается голос из ниоткуда, и опять звучит странный смех.')
            return False


