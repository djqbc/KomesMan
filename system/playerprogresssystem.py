from myevents import GAME_EVENT, GameEventType

class PlayerProgressSystem:
    NAME = "PlayerProgressSystem"
    def __init__(self):
        self.currentLevel = 1
    def register(self, _object):
        pass
    def remove(self, _entity):
        pass
    def update(self, _timeDelta, _systems):
        pass
    def input(self, _event):
        if _event.type == GAME_EVENT and _event.reason == GameEventType.WON_GAME:
            self.currentLevel += 1