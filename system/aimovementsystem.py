from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
import pygame

class AiMovementSystem:
    observing = []
    def __init__(self):
        pass
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def update(self, _delta):
        pass
    def input(self, _event):
        pass