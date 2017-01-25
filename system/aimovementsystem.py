from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagSubType, TagType
from pathfinder import Node
from sprite.mysprite import AnimationState
from system.gamesystem import GameSystem, GameState
from system.tagsystem import TagSystem


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
        elif TagArtifact.NAME in _object.artifacts and _object.artifacts[
            TagArtifact.NAME].subtype == TagSubType.PATHFINDER:
            self.pathFinder = _object
        else:
            raise NameError("ERROR!!!")

    def update(self, _delta, _systems):
        if _systems[GameSystem.NAME].getcurrentgamestate() != GameState.GAME:
            return
        tag_system = _systems[TagSystem.NAME]
        baits = tag_system.getentities(TagType.ITEM, TagSubType.BAIT)
        if len(baits) > 0:
            target = baits[0]
        else:
            target = tag_system.getentities(TagType.KOMESMAN)[0]

        board = tag_system.getentities(TagType.FIXED, TagSubType.BOARD)[0]
        x = target.artifacts[SpriteArtifact.NAME].positionX
        y = target.artifacts[SpriteArtifact.NAME].positionY
        i_x = int(round(x / board.tileSize))
        i_y = int(round(y / board.tileSize))
        # print('komesman jest w ', iX, ' ', iY)
        for cop in self.observing:  # pozniej otagowac grupy wrogow i dla kazdej z nich miec mozliwosc innego kontrolera
            movement_artifact = cop.artifacts[MovementArtifact.NAME]
            sprite_artifact = cop.artifacts[SpriteArtifact.NAME]
            if movement_artifact.target == None:
    
                copi_x = int(sprite_artifact.positionX / board.tileSize)  # to jest kiepskie jezeli idziemy w góre
                copi_y = int(sprite_artifact.positionY / board.tileSize)  # to jest kiepskie, jezeli idziemy w lewo!!!
    
                if sprite_artifact.positionX % board.tileSize != 0 and movement_artifact.movementVector[0] < 0:
                    copi_x += 1
                if sprite_artifact.positionY % board.tileSize != 0 and movement_artifact.movementVector[1] < 0:
                    copi_y += 1
    
                next_move = self.pathFinder.getnextmove(Node(copi_x, copi_y), Node(i_x, i_y))
    
                if copi_x == i_x and copi_y == i_y:
                    return
    
                # print('Cop is moving from: [{copX}, {copY}] to [{komX}, {komY}]. Next tile = [{nextX},{nextY}]'
                # .format(copX = copiX, copY = copiY, komX = iX, komY = iY, nextX=nextMove.x, nextY=nextMove.y))
    
                x_to_reach = next_move.x * board.tileSize
                y_to_reach = next_move.y * board.tileSize
                movement_artifact.target = (x_to_reach, y_to_reach)
                print('New target: ', movement_artifact.target, 'Current Pos: ', sprite_artifact.positionX, sprite_artifact.positionY)

                # print('X TO REACH {x}. ACTUAL X {actx}. Y TO REACH. {y} ACTUAL Y {acty}'.
                # format(actx=spriteArtifact.positionX,x=xToReach,acty=spriteArtifact.positionY,y=yToReach))
            else:
                x_to_reach, y_to_reach = movement_artifact.target

            movement_artifact.movementVector = [0, 0]
            maxShiftN = movement_artifact.speedModifier * _delta * -1;
            maxShiftP = movement_artifact.speedModifier * _delta * 1;
            if y_to_reach == int(sprite_artifact.positionY):
                if sprite_artifact.positionY != int(sprite_artifact.positionY):
                    sprite_artifact.positionY = int(sprite_artifact.positionY)
            elif y_to_reach < sprite_artifact.positionY and board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, 0, maxShiftN):
                sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_UP
                movement_artifact.movementVector[1] = -1
            elif y_to_reach > sprite_artifact.positionY and board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, 0, maxShiftP):
                sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_DOWN
                movement_artifact.movementVector[1] = 1
                 
            if x_to_reach == int(sprite_artifact.positionX):
                if sprite_artifact.positionX != int(sprite_artifact.positionX):
                    sprite_artifact.positionX = int(sprite_artifact.positionX)
            elif x_to_reach < sprite_artifact.positionX and board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, maxShiftN, 0):
                sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_LEFT
                movement_artifact.movementVector[0] = -1
            elif x_to_reach > sprite_artifact.positionX and board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, maxShiftP, 0):
                sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_RIGHT
                movement_artifact.movementVector[0] = 1


            if movement_artifact.movementVector != [0, 0]:
                d_x = movement_artifact.movementVector[0] * movement_artifact.speedModifier * _delta
                d_y = movement_artifact.movementVector[1] * movement_artifact.speedModifier * _delta
                if board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, d_x, d_y):
#                     print(sprite_artifact.positionX, sprite_artifact.positionY, d_x, d_y)
                    diff1 = sprite_artifact.positionX - x_to_reach
                    diff2 = sprite_artifact.positionX + d_x - x_to_reach
                    if diff1 * diff2 < 0:
                        sprite_artifact.positionX = x_to_reach
                    else:
                        sprite_artifact.positionX += d_x
                        
                    diff1 = sprite_artifact.positionY - y_to_reach
                    diff2 = sprite_artifact.positionY + d_y - y_to_reach
                    if diff1 * diff2 < 0:
                        sprite_artifact.positionY = y_to_reach
                    else:
                        sprite_artifact.positionY += d_y
                else:
                    print('Wrong move: ', sprite_artifact, movement_artifact.target, sprite_artifact.positionX, sprite_artifact.positionY, d_x, d_y)
            else:
                print("Erase target")
                movement_artifact.target = None

    def input(self, _event):
        pass
