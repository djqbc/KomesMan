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

class GameManager:
    '''Class managing game state''' 
    screen = None
    drawSystem = DrawSystem()
    userMoveSystem = UserMovementSystem()
    aiMoveSystem = AiMovementSystem()
    tagSystem = TagSystem()
    collisionSystem = CollisionSystem()
    gameSystem = GameSystem()
    menuSystem = MenuSystem()
    hudSystem = HUDSystem()
    allSystems = {
        hudSystem.NAME : hudSystem,
        tagSystem.NAME : tagSystem,
        collisionSystem.NAME : collisionSystem,
        userMoveSystem.NAME : userMoveSystem, 
        aiMoveSystem.NAME : aiMoveSystem, 
        drawSystem.NAME : drawSystem,
        gameSystem.NAME : gameSystem,
        menuSystem.NAME : menuSystem
        }#kolejnosc moze byc wazna
    builders = [
        BoardBuilder(allSystems),
        MenuBuilder(allSystems)
        ]
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1024, 768), 0, 32)
        pygame.display.set_caption('KomesMan')        
        self.init()
    
    def update(self, _timeDelta):
        '''Updates current game state'''
        for _, system in self.allSystems.items():
            system.update(_timeDelta, self.allSystems)
    
    def init(self):
        self.gameSystem.endInit()
    
    def render(self, _updateMidstep):
        '''Renders currect scene'''
        self.screen.fill(pygame.Color('black'))
        self.drawSystem.draw(self.screen)
        pygame.display.flip()
    
    def input(self, _event):
        for builder in self.builders:
            builder.input(_event)
        for _, system in self.allSystems.items():
            system.input(_event)
    
    def quit(self):
        return self.gameSystem.quit()