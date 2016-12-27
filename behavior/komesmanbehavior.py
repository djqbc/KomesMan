from myevents import COLLISION_EVENT, LOST_GAME_EVENT
from artifact.tagartifact import TagArtifact, TagType
import pygame

class KomesManBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.ENEMY:
                _postEventCallback(pygame.event.Event(LOST_GAME_EVENT))