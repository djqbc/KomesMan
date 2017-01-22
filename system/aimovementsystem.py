from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagSubType, TagType
from pathfinder import Node
from sprite.mysprite import AnimationState
from system.tagsystem import TagSystem
import pygame
from system.gamesystem import GameSystem, GameState

class AiMovementSystem:
    NAME = "AiMovementSystem"
    observing = []
    def __init__(self):
        self.pathFinder = None
    def remove(self, _entity):
        self.observing[:] = [entity for entity in self.observing if entity != _entity]
                
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        elif TagArtifact.NAME in _object.artifacts and _object.artifacts[TagArtifact.NAME].subtype == TagSubType.PATHFINDER:
            self.pathFinder = _object
        else:
            raise NameError("ERROR!!!")

    def update(self, _delta, _systems):
        if _systems[GameSystem.NAME].getCurrentGameState() != GameState.GAME:
            return
        tagSystem = _systems[TagSystem.NAME]
        baits = tagSystem.getEntities(TagType.ITEM, TagSubType.BAIT)
        if len(baits) > 0:
            target = baits[0]
        else:
            target = tagSystem.getEntities(TagType.KOMESMAN)[0]
            
        board = tagSystem.getEntities(TagType.FIXED, TagSubType.BOARD)[0]
        x = target.artifacts[SpriteArtifact.NAME].positionX
        y = target.artifacts[SpriteArtifact.NAME].positionY
        iX = int(round(x/board.tileSize))
        iY = int(round(y/board.tileSize))
        #print('komesman jest w ', iX, ' ', iY)
        for cop in self.observing:#pozniej otagowac grupy wrogow i dla kazdej z nich miec mozliwosc innego kontrolera
            spriteArtifact = cop.artifacts[SpriteArtifact.NAME]
            movementArtifact = cop.artifacts[MovementArtifact.NAME]

            copiX = int(spriteArtifact.positionX / board.tileSize) # to jest kiepskie jezeli idziemy w góre
            copiY = int(spriteArtifact.positionY / board.tileSize) # to jest kiepskie, jezeli idziemy w lewo!!!

            if spriteArtifact.positionX % board.tileSize != 0 and movementArtifact.movementVector[0] < 0:
                copiX += 1
            if spriteArtifact.positionY % board.tileSize != 0 and movementArtifact.movementVector[1] < 0:
                copiY += 1

            nextMove = self.pathFinder.getNextMove(Node(copiX, copiY), Node(iX, iY))

            if copiX == iX and copiY == iY:
                return

#                print('Cop is moving from: [{copX}, {copY}] to [{komX}, {komY}]. Next tile = [{nextX},{nextY}]'.format(copX = copiX, copY = copiY, komX = iX, komY = iY, nextX=nextMove.x, nextY=nextMove.y))

            xToReach = nextMove.x * board.tileSize
            yToReach = nextMove.y * board.tileSize

#                print('X TO REACH {x}. ACTUAL X {actx}. Y TO REACH. {y} ACTUAL Y {acty}'.format(actx=spriteArtifact.positionX,x=xToReach,acty=spriteArtifact.positionY,y=yToReach))

            movementArtifact.movementVector = [0, 0]

            if yToReach == int(spriteArtifact.positionY):
                #Jestesmy w dobrym Y, musimy ruszac sie po X
                if spriteArtifact.positionY != int(spriteArtifact.positionY):
#                        print('Round Y!!!')
                    spriteArtifact.positionY = int(spriteArtifact.positionY)
                    return
                if xToReach < spriteArtifact.positionX:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_LEFT
                    movementArtifact.movementVector[0] = -1
                if xToReach > spriteArtifact.positionX:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_RIGHT
                    movementArtifact.movementVector[0] = 1
            if xToReach == int(spriteArtifact.positionX):
                #jestesmy w dobrym X, musimy ruszac sie po Y
                if spriteArtifact.positionX != int(spriteArtifact.positionX):
                    spriteArtifact.positionX = int(spriteArtifact.positionX)
#                        print('Round X!!!')
                    return
                if yToReach < spriteArtifact.positionY:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_UP
                    movementArtifact.movementVector[1] = -1
                if yToReach > spriteArtifact.positionY:
                    spriteArtifact.sprite.currentAnimation = AnimationState.MOVE_DOWN
                    movementArtifact.movementVector[1] = 1


            if movementArtifact.movementVector != [0, 0]:
                dX = movementArtifact.movementVector[0] * movementArtifact.speedModifier * _delta
                dY = movementArtifact.movementVector[1] * movementArtifact.speedModifier * _delta
                if board.checkMove(spriteArtifact.positionX, spriteArtifact.positionY, dX, dY):
                    spriteArtifact.positionX += dX
                    spriteArtifact.positionY += dY
    def input(self, _event):
        pass