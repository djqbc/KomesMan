from myevents import COLLISION_EVENT, SCREEN_EFFECT_EVENT, ScreenEffectEvent, EventType, GAME_EVENT, GameEventType, \
    ENTITY_EFFECT_EVENT, EntityEffect
from artifact.tagartifact import TagArtifact, TagType
import pygame


class BeerBehavior:
    """
    Defines behaviour of Beer object on incoming events
    """
    @staticmethod
    def input(_event, _posteventcallback):
        """
        Reaction on incoming event.
        Currently handles only collision (deletes object from map, turns on drunkness,
        and plays proper sound)
        :param _event: event to process
        :param _posteventcallback: function to evaluate after processing input
        :return: nothing
        """
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _posteventcallback(
                    pygame.event.Event(ENTITY_EFFECT_EVENT, effect=EntityEffect.PLAY_SOUND, path="res/sound/beer.wav"))
                _posteventcallback(pygame.event.Event(SCREEN_EFFECT_EVENT, type=ScreenEffectEvent.BLUR, time=5000,
                                                      reason=EventType.START))
                _posteventcallback(
                    pygame.event.Event(GAME_EVENT, reason=GameEventType.REMOVE_OBJECT, reference=_event.me))
