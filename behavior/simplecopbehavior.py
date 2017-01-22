from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType, TagSubType
import pygame
from artifact.spriteartifact import SpriteArtifact
from artifact.behaviorartifact import BehaviorArtifact

class SimpleCopBehavior:
    def __init__(self):
        self.firstInformed = None

    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tagArtifact = entity.artifacts[TagArtifact.NAME]
            if tagArtifact.type == TagType.ENEMY and tagArtifact.subtype == TagSubType.SIMPLE_COP:
                self.firstInformed = True
                try:
                    if entity.artifacts[BehaviorArtifact.NAME].behavior.firstInformed:
                        self.firstInformed = False
                except:
                    pass
                if self.firstInformed:
                    spriteArtifact = entity.artifacts[SpriteArtifact.NAME]
                    _postEventCallback(pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
                    _postEventCallback(pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=entity))
                    _postEventCallback(pygame.event.Event(GAME_EVENT, reason=GameEventType.SPAWN_OBJECT, spawntype=TagType.ENEMY, 
                                          spawnsubtype=TagSubType.SUPER_COP, x=spriteArtifact.positionX, y=spriteArtifact.positionY))