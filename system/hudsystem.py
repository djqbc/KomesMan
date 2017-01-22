from artifact.spriteartifact import SpriteArtifact
from myevents import GAME_EVENT, GameEventType


class HUDSystem:  # zmienic nazwe kiedys - nie chcialo mi sie myslec nad lepsza
    NAME = "HUDSystem"
    observing = []
    dirty = True

    def __init__(self):
        self.observing = []

    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts:
            self.dirty = True
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def update(self, _timeDelta, _systems):
        pass

    def input(self, _event):
        if _event.type == GAME_EVENT and _event.reason == GameEventType.HUD_UPDATE:
            for entity in self.observing:
                entity.artifacts[SpriteArtifact.NAME].sprite.updateHUD(_event.caps, _event.lifes, _event.points)
            self.dirty = True
