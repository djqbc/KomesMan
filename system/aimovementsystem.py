from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from sprite.mysprite import AnimationState
from system.tagsystem import TagSystem
import pygame
from system.gamesystem import GameSystem, GameState

class AiMovementSystem:
    NAME = "AiMovementSystem"
    observing = []
    def __init__(self):
        pass
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
                
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")

    def update(self, _delta, _systems):
        if _systems[GameSystem.NAME].getCurrentGameState() != GameState.GAME:
            return
        tagSystem = _systems[TagSystem.NAME]
        entities = tagSystem.getEntities("KomesMan")
        board = tagSystem.getEntities("Board")[0]
        if entities != None:
            komesMan = entities[0]
            x = komesMan.artifacts[SpriteArtifact.NAME].positionX
            y = komesMan.artifacts[SpriteArtifact.NAME].positionY
            for cop in self.observing:#pozniej otagowac grupy wrogow i dla kazdej z nich miec mozliwosc innego kontrolera
                spriteArtifact = cop.artifacts[SpriteArtifact.NAME]
                movementArtifact = cop.artifacts[MovementArtifact.NAME]
                if spriteArtifact.positionX < x:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_RIGHT
                    movementArtifact.movementVector[0] = 1
                elif spriteArtifact.positionX > x:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_LEFT
                    movementArtifact.movementVector[0] = -1
                else:
                    movementArtifact.movementVector[0] = 0
                if spriteArtifact.positionY < y:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_DOWN
                    movementArtifact.movementVector[1] = 1
                elif spriteArtifact.positionY > y:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_UP
                    movementArtifact.movementVector[1] = -1
                else:
                    movementArtifact.movementVector[1] = 0
                
                if movementArtifact.movementVector != [0, 0]:
                    dX = movementArtifact.movementVector[0] * movementArtifact.speedModifier * _delta
                    dY = movementArtifact.movementVector[1] * movementArtifact.speedModifier * _delta
                    if board.checkMove(spriteArtifact.positionX, spriteArtifact.positionY, dX, dY):
                        spriteArtifact.positionX += dX
                        spriteArtifact.positionY += dY
    def input(self, _event):
        pass