from inventory import Inventory
from copy import deepcopy

class Effect:
    def __init__(self):
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
    def __init__(self, time):
        self.time = time

    def event(self, game, player, event):
        if event == "before_move":
            game.log("Вы пропускаете ход")
            game.next_move()
        else:
            super(Stun, self).event(game, player, event)

class Sleep(ExpiringEffect):
    def __init__(self, time, start_field, start_position):
        self.time = time
        self.start_field = start_field
        self.start_position = start_position

    def expire(self, game, player):
        game.log("Вы проснулись")
        player.position = self.asleep_position
        player.effects = self.asleep_effects
        player.inventory = self.asleep_inventory
        player.field = self.asleep_field
        game.log("Вот что на самом деле лежит в вашей сумке: {}".format(player.inventory))

    def event(self, game, player, event):
        super(Sleep, self).event(game, player, event)
        if event == "start":
            self.asleep_position = player.position
            self.asleep_inventory = deepcopy(player.inventory)
            self.asleep_effects = deepcopy(player.effects)
            self.asleep_field = player.field
            player.position = self.start_position
            player.field = self.start_field
        if event == "win":
            game.log("Какой приятный был сон!")
            self.expire(game, player)
            return True
        elif event == "die":
            game.log("Кошмар. Ну и приснится же такое!")
            self.expire(game, player)
            return True
