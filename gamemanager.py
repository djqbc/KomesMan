import pygame

from system.drawsystem import DrawSystem
from system.usermovementsystem import UserMovementSystem
from system.aimovementsystem import AiMovementSystem
from system.tagsystem import TagSystem
from system.collisionsystem import CollisionSystem
from system.gamesystem import GameSystem
from system.menusystem import MenuSystem
from system.hudsystem import HUDSystem
from builder.boardbuilder import BoardBuilder
from builder.menubuilder import MenuBuilder
from system.musicsystem import MusicSystem
from system.playerprogresssystem import PlayerProgressSystem


class GameManager:
    """Class managing game state"""
    drawSystem = DrawSystem()
    userMoveSystem = UserMovementSystem()
    aiMoveSystem = AiMovementSystem()
    tagSystem = TagSystem()
    collisionSystem = CollisionSystem()
    gameSystem = GameSystem()
    menuSystem = MenuSystem()
    hudSystem = HUDSystem()
    musicSystem = MusicSystem()
    playerProgressSystem = PlayerProgressSystem()
    allSystems = {
        hudSystem.NAME: hudSystem,
        tagSystem.NAME: tagSystem,
        collisionSystem.NAME: collisionSystem,
        userMoveSystem.NAME: userMoveSystem,
        drawSystem.NAME: drawSystem,
        gameSystem.NAME: gameSystem,
        menuSystem.NAME: menuSystem,
        musicSystem.NAME: musicSystem,
        playerProgressSystem.NAME: playerProgressSystem,
        aiMoveSystem.NAME: aiMoveSystem,
    }
    allSystemsForIteration = [item for item in allSystems.values()]# kolejnosc moze byc wazna < ale to mozna ogarnac tu a nie w slowniku..
    builders = [
        BoardBuilder(allSystems),
        MenuBuilder(allSystems)
    ]

    def __init__(self):
        pygame.init()
        self.init()

    def update(self, _timedelta):
        """Updates current game state"""
        for system in self.allSystemsForIteration:
            system.update(_timedelta, self.allSystems)

    def init(self):
        self.gameSystem.endinit()

    def render(self, _updatemidstep):
        """Renders currect scene"""
        self.drawSystem.draw()

    def input(self, _event):
        for builder in self.builders:
            builder.input(_event)
        for system in self.allSystemsForIteration:
             system.input(_event)

    def quit(self):
        return self.gameSystem.quit()
