from myevents import COLLISION_EVENT, REMOVE_OBJECT_EVENT, ENTITY_EFFECT_EVENT,\
    EntityEffect
from artifact.tagartifact import TagArtifact, TagType
import pygame

class CapBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                _postEventCallback(pygame.event.Event(ENTITY_EFFECT_EVENT, reference=entity, effect=EntityEffect.PICK_UP_CAP))
                _postEventCallback(pygame.event.Event(REMOVE_OBJECT_EVENT, reference=_event.me))