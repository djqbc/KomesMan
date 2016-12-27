from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from sprite.mysprite import AnimationState
from system.tagsystem import TagSystem
import pygame

class AiMovementSystem:
    NAME = "AiMovementSystem"
    observing = []
    def __init__(self):
        pass
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def update(self, _delta, _systems):
        tagSystem = _systems[TagSystem.NAME]
        entities = tagSystem.getEntities("KomesMan")
        board = tagSystem.getEntities("Board")[0]
        if entities != None:
            komesMan = entities[0]
            x = komesMan.artifacts[SpriteArtifact.NAME].positionX
            y = komesMan.artifacts[SpriteArtifact.NAME].positionY
            for cop in self.observing:#pozniej otagowac grupy wrogow i dla kazdej z nich miec mozliwosc innego kontrolera
                if cop.artifacts[SpriteArtifact.NAME].positionX < x:
                    cop.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_RIGHT
                    cop.artifacts[MovementArtifact.NAME].movementVector[0] = 1
                elif cop.artifacts[SpriteArtifact.NAME].positionX > x:
                    cop.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_LEFT
                    cop.artifacts[MovementArtifact.NAME].movementVector[0] = -1
                else:
                    cop.artifacts[MovementArtifact.NAME].movementVector[0] = 0
                if cop.artifacts[SpriteArtifact.NAME].positionY < y:
                    cop.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_DOWN
                    cop.artifacts[MovementArtifact.NAME].movementVector[1] = 1
                elif cop.artifacts[SpriteArtifact.NAME].positionY > y:
                    cop.artifacts[SpriteArtifact.NAME].sprite.currentAnimation = AnimationState.MOVE_UP
                    cop.artifacts[MovementArtifact.NAME].movementVector[1] = -1
                else:
                    cop.artifacts[MovementArtifact.NAME].movementVector[1] = 0
                
                if cop.artifacts[MovementArtifact.NAME].movementVector != [0, 0]:
                    dX = cop.artifacts[MovementArtifact.NAME].movementVector[0] * cop.artifacts[MovementArtifact.NAME].speedModifier
                    dY = cop.artifacts[MovementArtifact.NAME].movementVector[1] * cop.artifacts[MovementArtifact.NAME].speedModifier
                    if board.checkMove(cop.artifacts[SpriteArtifact.NAME].positionX, cop.artifacts[SpriteArtifact.NAME].positionY, dX, dY):
                        cop.artifacts[SpriteArtifact.NAME].positionX += dX
                        cop.artifacts[SpriteArtifact.NAME].positionY += dY
    def input(self, _event):
        pass