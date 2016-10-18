from .effect import Effect, ExpiringEffect
from copy import deepcopy
from inventory import Inventory


class Sleep(Effect):

    def __init__(self, time, start_position):
        self.time = time
        self.start_position = start_position

    def expire(self, game, player):
        game.players.remove(self.spirit)
        self._expire(player)
        player.active = True
        game.log("Вот что на самом деле лежит в вашей сумке: {}".format(
            player.inventory))

    def event(self, game, player, event):
        super(Sleep, self).event(game, player, event)
        if event == "start":
            self.spirit = deepcopy(player)
            self.spirit.effects.pop()  # remove this effect
            self.spirit.position = self.start_position
            self.spirit.add_effect(game, Dream(self.time, self, player))
            game.players.insert(game.current_player, self.spirit)
            player.active = False
        elif event == "die":
            self.expire(game, player)
            return False


class Dream(ExpiringEffect):

    def __init__(self, time, sleep_effect, body):
        self.time = time
        self.sleep_effect = sleep_effect
        self.body = body

    def expire(self, game, player):
        game.log(player, "Вы проснулись")
        self.sleep_effect.expire(game, self.body)

    def event(self, game, player, event):
        super(Dream, self).event(game, player, event)
        if event == "win":
            game.log("Какой приятный был сон!")
            self.expire(game, player)
            return True
        elif event == "die":
            game.log("Кошмар. Ну и приснится же такое!")
            self.expire(game, player)
            return True
