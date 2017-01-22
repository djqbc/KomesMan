from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame


class KomesManBehavior:
    @staticmethod
    def input(_event, _posteventcallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tag_artifact = entity.artifacts[TagArtifact.NAME]
            if tag_artifact.type == TagType.ENEMY:
                _posteventcallback(pygame.event.Event(GAME_EVENT, reason=GameEventType.LOST_LIFE))
