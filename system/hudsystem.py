"""HudSystem module."""
from artifact.spriteartifact import SpriteArtifact
from myevents import GAME_EVENT, GameEventType


class HUDSystem:
    """System responsible for updating HUD."""

    NAME = "HUDSystem"
    observing = []
    dirty = True

    def __init__(self):
        """Constructor."""
        self.observing = []

    def register(self, _object):
        """
        Register aprite objects to the system.

        :param _object: Sprite object
        :return: nothing
        """
        if SpriteArtifact.NAME in _object.artifacts:
            self.dirty = True
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def remove(self, _entity):
        """
        Remove object from system.

        :param _entity: Entity to be removed
        :return: nothing
        """
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def update(self, _timedelta, _systems):
        """
        Stub method for updating system.

        :param _timedelta: time delta of game loop
        :param _systems: collection of all systems.
        :return:
        """
        pass

    def input(self, _event):
        """
        Process input for HUD sytem.

        Updates system with new data from event.
        :param _event: Event for processing
        :return: nothing
        """
        if _event.type == GAME_EVENT and _event.reason == GameEventType.HUD_UPDATE:
            for entity in self.observing:
                entity.artifacts[SpriteArtifact.NAME].sprite.updatehud(_event.caps, _event.lifes, _event.points)
            self.dirty = True
