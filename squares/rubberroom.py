from .square import Square

class RubberRoom(Square):
    def __init__(self, direction):
        super(RubberRoom, self).__init__()
        self.direction = direction

    def can_move(self, game, player, direction):
        if direction == self.direction:
            game.log("Вы вышли из резиновой комнаты")
            return None
        return True


