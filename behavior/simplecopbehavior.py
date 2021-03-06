"""Simple cop behaviour package."""
from myevents import COLLISION_EVENT, GAME_EVENT, GameEventType
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from artifact.spriteartifact import SpriteArtifact
from artifact.behaviorartifact import BehaviorArtifact
import pygame


class SimpleCopBehavior:
    """Class defining behaviour of standard cop on incoming events."""

    def __init__(self):
        """Constructor."""
        self.firstinformed = None

    def input(self, _event, _posteventcallback):
        """
        Reaction on incoming event.

        On collision with another cop, changes itself into new super-cop (which is faster)
        :param _event: event to process
        :param _posteventcallback: function to evaluate after processing input
        :return: nothing
        """
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            tag_artifact = entity.artifacts[TagArtifact.NAME]
            if tag_artifact.type == TagType.ENEMY and tag_artifact.subtype == TagSubType.SIMPLE_COP:
                self.firstinformed = True
                try:
                    if entity.artifacts[BehaviorArtifact.NAME].behavior.firstInformed:
                        self.firstinformed = False
                except:
                    pass
                if self.firstinformed:
                    sprite_artifact = entity.artifacts[SpriteArtifact.NAME]
                    _posteventcallback(
                        pygame.event.Event(GAME_EVENT
                                           , reason=GameEventType.REMOVE_OBJECT
                                           , reference=_event.me))
                    _posteventcallback(
                        pygame.event.Event(GAME_EVENT
                                           , reason=GameEventType.REMOVE_OBJECT, reference=entity))
                    _posteventcallback(
                        pygame.event.Event(GAME_EVENT
                                           , reason=GameEventType.SPAWN_OBJECT
                                           , spawntype=TagType.ENEMY,
                                           spawnsubtype=TagSubType.SUPER_COP
                                           , x=int(sprite_artifact.positionx),
                                           y=int(sprite_artifact.positiony)))
