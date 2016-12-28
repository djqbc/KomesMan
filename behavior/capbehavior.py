from myevents import COLLISION_EVENT, REMOVE_OBJECT_EVENT
from artifact.tagartifact import TagArtifact, TagType
import pygame

class CapBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                ##jakies zdarzenie do zbierania punktow - dorobic system ktory to obsluzy
                _postEventCallback(pygame.event.Event(REMOVE_OBJECT_EVENT, reference=_event.me))