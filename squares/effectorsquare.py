from .square import Square

class EffectorSquare(Square):
    def __init__(self, effect_class, message=None):
        super(EffectorSquare, self).__init__(message)
        self.effect_class = effect_class

    def event(self, game, player, event):
        super(EffectorSquare, self).event(game, player, event)
        if event == "arrive":
            player.add_effect(game, self.effect_class())


