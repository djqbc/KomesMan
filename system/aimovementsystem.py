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
            sprite_artifact = cop.artifacts[SpriteArtifact.NAME]
            movement_artifact = cop.artifacts[MovementArtifact.NAME]

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

            # print('X TO REACH {x}. ACTUAL X {actx}. Y TO REACH. {y} ACTUAL Y {acty}'.
            # format(actx=spriteArtifact.positionX,x=xToReach,acty=spriteArtifact.positionY,y=yToReach))

            movement_artifact.movementVector = [0, 0]

            if y_to_reach == int(sprite_artifact.positionY):
                # Jestesmy w dobrym Y, musimy ruszac sie po X
                if sprite_artifact.positionY != int(sprite_artifact.positionY):
                    #                        print('Round Y!!!')
                    sprite_artifact.positionY = int(sprite_artifact.positionY)
                    return
                if x_to_reach < sprite_artifact.positionX:
                    sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_LEFT
                    movement_artifact.movementVector[0] = -1
                if x_to_reach > sprite_artifact.positionX:
                    sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_RIGHT
                    movement_artifact.movementVector[0] = 1
            if x_to_reach == int(sprite_artifact.positionX):
                # jestesmy w dobrym X, musimy ruszac sie po Y
                if sprite_artifact.positionX != int(sprite_artifact.positionX):
                    sprite_artifact.positionX = int(sprite_artifact.positionX)
                    #                        print('Round X!!!')
                    return
                if y_to_reach < sprite_artifact.positionY:
                    sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_UP
                    movement_artifact.movementVector[1] = -1
                if y_to_reach > sprite_artifact.positionY:
                    sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_DOWN
                    movement_artifact.movementVector[1] = 1

            if movement_artifact.movementVector != [0, 0]:
                d_x = movement_artifact.movementVector[0] * movement_artifact.speedModifier * _delta
                d_y = movement_artifact.movementVector[1] * movement_artifact.speedModifier * _delta
                if board.checkmove(sprite_artifact.positionX, sprite_artifact.positionY, d_x, d_y):
                    sprite_artifact.positionX += d_x
                    sprite_artifact.positionY += d_y

    def input(self, _event):
        pass
