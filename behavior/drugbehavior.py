from myevents import COLLISION_EVENT, REMOVE_OBJECT_EVENT, SCREEN_EFFECT_EVENT, ENTITY_EFFECT_EVENT, ScreenEffectEvent, EventType,\
    EntityEffect
from artifact.tagartifact import TagArtifact, TagType
import pygame

class DrugBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _postEventCallback(pygame.event.Event(SCREEN_EFFECT_EVENT, type=ScreenEffectEvent.COLOR_EXPLOSION, time=4000, reason=EventType.START))
                _postEventCallback(pygame.event.Event(ENTITY_EFFECT_EVENT, reference=entity, reason=EventType.START, effect=EntityEffect.SPEED_CHANGE, modifier=2, time=5000))
                _postEventCallback(pygame.event.Event(REMOVE_OBJECT_EVENT, reference=_event.me))