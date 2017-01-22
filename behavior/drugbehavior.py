from myevents import COLLISION_EVENT, GAME_EVENT, SCREEN_EFFECT_EVENT, ENTITY_EFFECT_EVENT, ScreenEffectEvent, \
    EventType, \
    EntityEffect, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame


class DrugBehavior:
    @staticmethod
    def input(_event, _posteventcallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _posteventcallback(
                    pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/snort.wav"))
                _posteventcallback(
                    pygame.event.Event(SCREEN_EFFECT_EVENT, type=ScreenEffectEvent.COLOR_EXPLOSION, time=4000,
                                       reason=EventType.START))
                _posteventcallback(pygame.event.Event(ENTITY_EFFECT_EVENT, reference=entity, reason=EventType.START,
                                                      effect=EntityEffect.SPEED_CHANGE, modifier=2, time=5000))
                _posteventcallback(
                    pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
