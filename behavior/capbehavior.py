from myevents import COLLISION_EVENT, GAME_EVENT, ENTITY_EFFECT_EVENT, EntityEffect, GameEventType
from artifact.tagartifact import TagArtifact, TagType
import pygame


class CapBehavior:
    @staticmethod
    def input(_event, _posteventcallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _posteventcallback(pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND,
                                                      path="res/sound/beer_szmitek.wav"))
                _posteventcallback(
                    pygame.event.Event(ENTITY_EFFECT_EVENT, reference=entity, effect=EntityEffect.PICK_UP_CAP))
                _posteventcallback(
                    pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
