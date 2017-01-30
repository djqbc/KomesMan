"""
AIMovementSystem module
"""
from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagSubType, TagType
from pathfinder import Node
from sprite.mysprite import AnimationState
from system.gamesystem import GameSystem, GameState
from system.tagsystem import TagSystem


class AiMovementSystem:
    """
    System repsonsible for moves of computer players.
    """
    NAME = "AiMovementSystem"
    observing = []

    def __init__(self):
        """
        COnstructor
        """
        self.pathfinder = None

    def remove(self, _entity):
        """
        Remove entity from entities observed by system.
        :param _entity:  Entity to remove
        :return: nothing
        """
        self.observing[:] = [entity for entity in self.observing if entity != _entity]

    def register(self, _object):
        """
        Add object to system
        :param _object: Movable object, or Pathginder
        :return: nothing
        """
        if SpriteArtifact.NAME in _object.artifacts and MovementArtifact.NAME in _object.artifacts:
            self.observing.append(_object)
        elif TagArtifact.NAME in _object.artifacts and _object.artifacts[
            TagArtifact.NAME].subtype == TagSubType.PATHFINDER:
            self.pathfinder = _object
        else:
            raise NameError("ERROR!!!")

    def update(self, _delta, _systems):
        """
        Creates move for AI players.
        If any bait exists, it is considered as a target, otherwise KomesMan is chased
        Another step is taken from Pathfinder, from tile to desired other tile.
        Movement vector is created, and later altered by modifiers (power-ups).
        At the end step is executed.
        :param _delta: Game loop delta.
        :param _systems: Collection of all game systems
        :return:
        """
        if _systems[GameSystem.NAME].getcurrentgamestate() != GameState.GAME:
            return
        tag_system = _systems[TagSystem.NAME]
        baits = tag_system.getentities(TagType.ITEM, TagSubType.BAIT)
        if len(baits) > 0:
            target = baits[0]
        else:
            target = tag_system.getentities(TagType.KOMESMAN)[0]

        board = tag_system.getentities(TagType.FIXED, TagSubType.BOARD)[0]
        tmp_x = target.artifacts[SpriteArtifact.NAME].positionx
        tmp_y = target.artifacts[SpriteArtifact.NAME].positiony
        i_x = int(round(tmp_x / board.tile_size))
        i_y = int(round(tmp_y / board.tile_size))
        # print('komesman jest w ', iX, ' ', iY)
        for cop in self.observing:
            movement_artifact = cop.artifacts[MovementArtifact.NAME]
            sprite_artifact = cop.artifacts[SpriteArtifact.NAME]
            if movement_artifact.target is None:
                copi_x = int(sprite_artifact.positionx / board.tile_size)
                copi_y = int(sprite_artifact.positiony / board.tile_size)
                if sprite_artifact.positionx % board.tile_size != 0 and movement_artifact.movementVector[0] < 0:
                    copi_x += 1
                if sprite_artifact.positiony % board.tile_size != 0 and movement_artifact.movementVector[1] < 0:
                    copi_y += 1
                next_move = self.pathfinder.getnextmove(Node(copi_x, copi_y), Node(i_x, i_y))
                if copi_x == i_x and copi_y == i_y:
                    return

                x_to_reach = next_move.node_x * board.tile_size
                y_to_reach = next_move.node_y * board.tile_size
                movement_artifact.target = (x_to_reach, y_to_reach)
            else:
                x_to_reach, y_to_reach = movement_artifact.target

            movement_artifact.movementVector = [0, 0]
            max_shift_n = movement_artifact.speedmodifier * _delta * -1
            max_shift_p = movement_artifact.speedmodifier * _delta * 1
            if y_to_reach == int(sprite_artifact.positiony):
                if sprite_artifact.positiony != int(sprite_artifact.positiony):
                    sprite_artifact.positiony = int(sprite_artifact.positiony)
            elif y_to_reach < sprite_artifact.positiony and board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, 0, max_shift_n):
                sprite_artifact.sprite.currentAnimation = AnimationState.MOVE_UP
                movement_artifact.movementVector[1] = -1
            elif y_to_reach > sprite_artifact.positiony and board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, 0, max_shift_p):
                sprite_artifact.sprite.currentanimation = AnimationState.MOVE_DOWN
                movement_artifact.movementVector[1] = 1

            if x_to_reach == int(sprite_artifact.positionx):
                if sprite_artifact.positionx != int(sprite_artifact.positionx):
                    sprite_artifact.positionx = int(sprite_artifact.positionx)
            elif x_to_reach < sprite_artifact.positionx and board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, max_shift_n, 0):
                sprite_artifact.sprite.currentanimation = AnimationState.MOVE_LEFT
                movement_artifact.movementVector[0] = -1
            elif x_to_reach > sprite_artifact.positionx and board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, max_shift_p, 0):
                sprite_artifact.sprite.currentanimation = AnimationState.MOVE_RIGHT
                movement_artifact.movementVector[0] = 1


            if movement_artifact.movementVector != [0, 0]:
                d_x = movement_artifact.movementVector[0] * movement_artifact.speedmodifier * _delta
                d_y = movement_artifact.movementVector[1] * movement_artifact.speedmodifier * _delta
                if board.checkmove(sprite_artifact.positionx, sprite_artifact.positiony, d_x, d_y):
#                     print(sprite_artifact.positionX, sprite_artifact.positionY, d_x, d_y)
                    diff1 = sprite_artifact.positionx - x_to_reach
                    diff2 = sprite_artifact.positionx + d_x - x_to_reach
                    if diff1 * diff2 < 0:
                        sprite_artifact.positionx = x_to_reach
                    else:
                        sprite_artifact.positionx += d_x

                    diff1 = sprite_artifact.positiony - y_to_reach
                    diff2 = sprite_artifact.positiony + d_y - y_to_reach
                    if diff1 * diff2 < 0:
                        sprite_artifact.positiony = y_to_reach
                    else:
                        sprite_artifact.positiony += d_y
                else:
                    print('Wrong move: ', sprite_artifact, movement_artifact.target, sprite_artifact.positionx, sprite_artifact.positiony, d_x, d_y)
            else:
#                 print("Erase target")
                movement_artifact.target = None

    def input(self, _event):
        """
        :param _event: event variable
        :return : nothing
        """
        pass
