from myevents import COLLISION_EVENT, SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType, GAME_EVENT, GameEventType, \
    ENTITY_EFFECT_EVENT, EntityEffect
from artifact.tagartifact import TagArtifact, TagType
import pygame


class BeerBehavior:
    @staticmethod
    def input(_event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _postEventCallback(
                    pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/beer.wav"))
                _postEventCallback(pygame.event.Event(SCREEN_EFFECT_EVENT, type=ScreenEffectEvent.BLUR, time=5000,
                                                      reason=EventType.START))
                _postEventCallback(
                    pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
