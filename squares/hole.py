from .square import Square

class Hole(Square):
    def __init__(self, target):
        super(Hole, self).__init__()
        self.target = target

    def event(self, game, player, event):
        super(Hole, self).event(game, player, event)
        if event == "arrive":
            game.log(player, "Вы попали в ДЫРУ.")
            player.position = self.target


