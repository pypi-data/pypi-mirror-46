from gym_holdem.holdem.table import Table


class Game:
    def __init__(self, players):
        self.table = Table()
        for p in players:
            self.table.add_player(p)
