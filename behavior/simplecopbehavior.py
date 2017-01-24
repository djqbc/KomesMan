from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType, TagSubType
import pygame
from artifact.spriteartifact import SpriteArtifact
from artifact.behaviorartifact import BehaviorArtifact


class SimpleCopBehavior:
    def __init__(self):
        self.firstInformed = None

    def input(self, _event, _posteventcallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tag_artifact = entity.artifacts[TagArtifact.NAME]
            if tag_artifact.type == TagType.ENEMY and tag_artifact.subtype == TagSubType.SIMPLE_COP:
                self.firstInformed = True
                try:
                    if entity.artifacts[BehaviorArtifact.NAME].behavior.firstInformed:
                        self.firstInformed = False
                except:
                    pass
                if self.firstInformed:
                    sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                    _posteventcallback(
                        pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
                    _posteventcallback(
                        pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=entity))
                    _posteventcallback(
                        pygame.event.Event(GAME_EVENT, reason=GameEventType.SPAWN_OBJECT, spawntype=TagType.ENEMY,
                                           spawnsubtype=TagSubType.SUPER_COP, x=int(sprite_artifact.positionX),
                                           y=int(sprite_artifact.positionY)))
