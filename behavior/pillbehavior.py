from myevents import COLLISION_EVENT, GAME_EVENT, ENTITY_EFFECT_EVENT, EventType, \
    EntityEffect, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame


class PillBehavior:
    @staticmethod
    def input(_event, _posteventcallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _posteventcallback(pygame.event.Event(ENTITY_EFFECT_EVENT, reference=entity, reason=EventType.START,
                                                      effect=EntityEffect.SPEED_CHANGE, modifier=2, time=2000))
                _posteventcallback(pygame.event.Event(ENTITY_EFFECT_EVENT, reference=entity, reason=EventType.DELAYED,
                                                      effect=EntityEffect.SPEED_CHANGE, modifier=0.5, delay=2010,
                                                      time=2000))
                _posteventcallback(
                    pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
