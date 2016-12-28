from myevents import COLLISION_EVENT, REMOVE_OBJECT_EVENT, SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType
from artifact.tagartifact import TagArtifact, TagType
import pygame

class BeerBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _postEventCallback(pygame.event.Event(SCREEN_EFFECT_EVENT, type=ScreenEffectEvent.BLUR, time=5000, reason=EventType.START))
                _postEventCallback(pygame.event.Event(REMOVE_OBJECT_EVENT, reference=_event.me))