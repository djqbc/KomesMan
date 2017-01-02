from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame

class KomesManBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tagArtifact = entity.artifacts[TagArtifact.NAME]
            if tagArtifact.type == TagType.ENEMY:
                _postEventCallback(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_LIFE))     
