class Effect:
    def event(self, game, player, event):
        pass

    def _expire(self, player):
        player.effects.remove(self)

class ExpiringEffect(Effect):
    time = 1

    def __init__(self):
        self.time = type(self).time

    def expire(self, game, player):
        pass

    def event(self, game, player, event):
        if event == "move":
            self.time -= 1
            if self.time == 0:
                self.expire(game, player)
                self._expire(player)

class Stun(ExpiringEffect):
    def __init__(self, time):
        self.time = time

    def event(self, game, player, event):
        if event == "before_move":
            game.log("Вы пропускаете ход")
            game.next_move()
        else:
            super(Stun, self).event(game, player, event)
