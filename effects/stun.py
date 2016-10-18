from .effect import Effect


class Stun(Effect):

    def __init__(self, time):
        self.time = time

    def event(self, game, player, event):
        if event == "before_move":
            game.log("Вы пропускаете ход")
            self.time -= 1
            if self.time == 0:
                self._expire(player)
            game.next_move()
        else:
            super(Stun, self).event(game, player, event)
