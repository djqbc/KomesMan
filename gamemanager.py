"""GameManager module."""

import pygame

from system.drawsystem import DrawSystem
from system.usermovementsystem import UserMovementSystem
from system.aimovementsystem import AiMovementSystem
from system.tagsystem import TagSystem
from system.collisionsystem import CollisionSystem
from system.gamesystem import GameSystem
from system.menusystem import MenuSystem
from system.hudsystem import HUDSystem
from system.musicsystem import MusicSystem
from system.playerprogresssystem import PlayerProgressSystem
from builder.boardbuilder import BoardBuilder
from builder.menubuilder import MenuBuilder


class GameManager:
    """Class processing game loop."""

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
    allSystemsForIteration = [item for item in allSystems.values()]
    builders = [
        BoardBuilder(allSystems),
        MenuBuilder(allSystems)
    ]

    def __init__(self):
        """Constructor. Initializes pyGame."""
        pygame.init()
        self.init()

    def update(self, _timedelta):
        """
        Update current game state.

        :param _timedelta: game loop time delta
        :return:
        """
        for system in self.allSystemsForIteration:
            system.update(_timedelta, self.allSystems)

    def init(self):
        """
        End initialization of game system.

        :return:
        """
        self.gameSystem.endinit()

    def render(self):
        """
        Render current scene.

        :return: nothing
        """
        self.drawSystem.draw()

    def input(self, _event):
        """
        Process input through all systems.

        All systems go !!!
        :param _event: event to be processed by all systems !
        :return: nothing
        """
        for builder in self.builders:
            builder.input(_event)
        for system in self.allSystemsForIteration:
            system.input(_event)

    def quit(self):
        """
        Quit game.

        :return: nothing
        """
        return self.gameSystem.quit()
