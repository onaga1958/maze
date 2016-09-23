from inventory import Inventory

class Effect:
    def __init__(self, game, player):
        pass

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
    def __init__(self, game, player, time):
        self.time = time

    def event(self, game, player, event):
        if event == "before_move":
            game.log("Вы пропускаете ход")
            game.next_move()
        else:
            super(Stun, self).event(game, player, event)
=`=jedi=0, =`=                 (*_*game*_*, player, time) =`=jedi=`=
class Sleep(ExpiringEffect):
    time = 4
    start_position = (0, 0)

    def __init__(self, game, player, time):
        self.asleep_position = player.position
        self.asleep_inventory = Inventory(player.inventory)
        self.asleep_effects = player.effects[:]
        player.position = self.start_position

    def expire(self, game, player):
        game.log("Вы проснулись")
        player.position = self.asleep_position
        player.effects = self.asleep_effects
        player.inventory = player.asleep_inventory
        game.log("Вот что на самом деле лежит в вашей сумке: {}".format(player.inventory))

    def event(self, game, player, event):
        super(Sleep, self).event(game, player, event)
        if event == "win":
            game.log("Какой приятный был сон!")
            self.expire(game, player)
            return True
        elif event == "die":
            game.log("Ну и приснится же такое!")
            self.expire(game, player)
            return True
