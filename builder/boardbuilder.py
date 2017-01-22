import pygame

from binaryboarditemsgetter import BinaryBoardItemsGetter
from binaryboardtospritesconverter import BinaryBoardToSpritesConverter
from board import Board
from pathfinder import Pathfinder
from predefinedboard import PredefinedBoard
from sprite.komesmansprite import KomesManSprite
from sprite.copsprite import CopSprite
from entity import Entity
from artifact.movementartifact import MovementArtifact
from artifact.spriteartifact import SpriteArtifact
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from artifact.behaviorartifact import BehaviorArtifact
from behavior.simplecopbehavior import SimpleCopBehavior
from behavior.komesmanbehavior import KomesManBehavior
from system.gamesystem import GameState
from sprite.beersprite import BeerSprite
from behavior.beerbehavior import BeerBehavior
from sprite.drugsprite import DrugSprite
from behavior.drugbehavior import DrugBehavior
from sprite.capsprite import CapSprite
from behavior.capbehavior import CapBehavior
from system.aimovementsystem import AiMovementSystem
from system.collisionsystem import CollisionSystem
from myevents import GAME_EVENT, GameEventType
from system.tagsystem import TagSystem
from system.usermovementsystem import UserMovementSystem
from system.drawsystem import DrawSystem
from myevents import MENU_EVENT, MenuEventType
from generatedboard import GeneratedBoard
from system.playerprogresssystem import PlayerProgressSystem
from sprite.pillsprite import PillSprite
from behavior.pillbehavior import PillBehavior
import time
from sprite.dummysprite import DummySprite
from behavior.teleportbehavior import TeleportBehavior
from sprite.baitsprite import BaitSprite
from behavior.baitbehavior import BaitBehavior

class BoardBuilder:
    def __init__(self, _systems):
        self.systems = _systems
        self.elements = []
        self.binaryboard = None

    def build(self, _restart=False):
        if not _restart:
            if self.systems[PlayerProgressSystem.NAME].currentLevel == 1:
                self.binaryboard = PredefinedBoard().get_board_binary()
            else:
                self.binaryboard = GeneratedBoard().get_board_binary()

        self.createBoard(BinaryBoardToSpritesConverter().convert(self.binaryboard))

        itemsgetter = BinaryBoardItemsGetter()
        itemsgetter.loadItems(self.binaryboard)

        pygame.event.post(pygame.event.Event(GAME_EVENT, reason=GameEventType.SET_MAX_POINTS, maxPoints=len(itemsgetter.caps)))

        tileSize = 64 #to da sie pewno skads wziac?

        for pill in itemsgetter.pills:
            self.createPill(pill[0]*tileSize, pill[1]*tileSize)
        for cap in itemsgetter.caps:
            self.createCap(cap[0]*tileSize, cap[1]*tileSize)
        for amph in itemsgetter.amphs:
            self.createDrug(amph[0]*tileSize, amph[1]*tileSize)
        for beer in itemsgetter.beers:
            self.createBeer(beer[0]*tileSize, beer[1]*tileSize)
        for enemy in itemsgetter.enemies:
            self.createCop(enemy[0]*tileSize, enemy[1]*tileSize)
        self.createKomesMan(itemsgetter.komesman[0]*tileSize, itemsgetter.komesman[1]*tileSize)
        for teleport in itemsgetter.teleports:
            self.createTeleport(teleport[0]*tileSize, teleport[1]*tileSize)
        
    def clear(self):
        for e in self.elements:
            for _, system in self.systems.items():
                system.remove(e)
        self.elements.clear()
    def input(self, _event):
        if _event.type == MENU_EVENT:
            if _event.action == MenuEventType.START_NEW_GAME or _event.action == MenuEventType.CONTINUE_GAME:
                self.clear()
                self.build()
            elif _event.action == MenuEventType.RESTART_GAME:
                self.clear()
                self.build(True)
        elif _event.type == GAME_EVENT: 
            if _event.reason == GameEventType.REMOVE_OBJECT:
                self.elements.remove(_event.reference)
                for _, system in self.systems.items():
                    system.remove(_event.reference)
            elif _event.reason == GameEventType.SPAWN_OBJECT:
                if _event.spawntype == TagType.ENEMY and _event.spawnsubtype == TagSubType.SUPER_COP:
                    self.createSuperCop(_event.x, _event.y)
                elif _event.spawntype == TagType.ITEM and _event.spawnsubtype == TagSubType.BAIT:
                    self.createBait(_event.x, _event.y)
            
    def createKomesMan(self, x, y):
        komesMan = Entity()
        komesMan.addArtifact(SpriteArtifact(KomesManSprite(), x, y, GameState.GAME))
        komesMan.addArtifact(MovementArtifact())
        komesMan.addArtifact(TagArtifact(TagType.KOMESMAN))
        komesMan.addArtifact(BehaviorArtifact(KomesManBehavior()))
        self.systems[TagSystem.NAME].register(komesMan)
        self.systems[UserMovementSystem.NAME].register(komesMan)
        self.systems[DrawSystem.NAME].register(komesMan)
        self.systems[CollisionSystem.NAME].register(komesMan)
        self.elements.append(komesMan)
        
    def createCop(self, _x, _y):
        cop = Entity()
        cop.addArtifact(SpriteArtifact(CopSprite(), _x, _y, GameState.GAME))
        cop.addArtifact(MovementArtifact(1))
        cop.addArtifact(TagArtifact(TagType.ENEMY, TagSubType.SIMPLE_COP))
        cop.addArtifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)
    
    def createSuperCop(self, _x, _y):
        cop = Entity()
        cop.addArtifact(SpriteArtifact(CopSprite(), _x, _y, GameState.GAME))
        cop.addArtifact(MovementArtifact(1.5))
        cop.addArtifact(TagArtifact(TagType.ENEMY, TagSubType.SUPER_COP))
        cop.addArtifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)
        
    def createBeer(self, _x, _y):
        beer = Entity()
        beer.addArtifact(SpriteArtifact(BeerSprite(), _x, _y, GameState.GAME))
        beer.addArtifact(TagArtifact(TagType.ITEM, TagSubType.BEER))
        beer.addArtifact(BehaviorArtifact(BeerBehavior()))
        self.systems[DrawSystem.NAME].register(beer)
        self.systems[TagSystem.NAME].register(beer)
        self.systems[CollisionSystem.NAME].register(beer)
        self.elements.append(beer)
        
    def createBait(self, _x, _y):
        bait = Entity()
        bait.addArtifact(SpriteArtifact(BaitSprite(), _x, _y, GameState.GAME))
        bait.addArtifact(TagArtifact(TagType.ITEM, TagSubType.BAIT))
        bait.addArtifact(BehaviorArtifact(BaitBehavior()))
        self.systems[DrawSystem.NAME].register(bait)
        self.systems[TagSystem.NAME].register(bait)
        self.systems[CollisionSystem.NAME].register(bait)
        self.elements.append(bait)
    
    def createDrug(self, _x, _y):
        drug = Entity()
        drug.addArtifact(SpriteArtifact(DrugSprite(), _x, _y, GameState.GAME))
        drug.addArtifact(TagArtifact(TagType.ITEM, TagSubType.DRUG))
        drug.addArtifact(BehaviorArtifact(DrugBehavior()))
        self.systems[DrawSystem.NAME].register(drug)
        self.systems[TagSystem.NAME].register(drug)
        self.systems[CollisionSystem.NAME].register(drug)
        self.elements.append(drug)
        
    def createCap(self, _x, _y):
        cap = Entity()
        cap.addArtifact(SpriteArtifact(CapSprite(), _x, _y, GameState.GAME))
        cap.addArtifact(TagArtifact(TagType.ITEM, TagSubType.CAP))
        cap.addArtifact(BehaviorArtifact(CapBehavior()))
        self.systems[DrawSystem.NAME].register(cap)
        self.systems[TagSystem.NAME].register(cap)
        self.systems[CollisionSystem.NAME].register(cap)
        self.elements.append(cap)
        
    def createTeleport(self, _x, _y):
        teleport = Entity()
        teleport.addArtifact(SpriteArtifact(DummySprite(), _x, _y, GameState.GAME))
        teleport.addArtifact(TagArtifact(TagType.FIXED, TagSubType.TELEPORT))
        teleport.addArtifact(BehaviorArtifact(TeleportBehavior()))
        self.systems[DrawSystem.NAME].register(teleport)
        self.systems[TagSystem.NAME].register(teleport)
        self.systems[CollisionSystem.NAME].register(teleport)
        self.elements.append(teleport)
        
    def createPill(self, _x, _y):
        pill = Entity()
        pill.addArtifact(SpriteArtifact(PillSprite(), _x, _y, GameState.GAME))
        pill.addArtifact(TagArtifact(TagType.ITEM, TagSubType.PILL))
        pill.addArtifact(BehaviorArtifact(PillBehavior()))
        self.systems[DrawSystem.NAME].register(pill)
        self.systems[TagSystem.NAME].register(pill)
        self.systems[CollisionSystem.NAME].register(pill)
        self.elements.append(pill)

    def createBoard(self, predefinedboard):
        #kijowe bezposrednie przekazanie elements - mozna olac jak nikomu sie nie bedzie chcialo poprawic
        Board(predefinedboard, self.systems, self.elements)
        start = int(round(time.time() * 1000))
        pf = Pathfinder(predefinedboard)
        pf.prepareAllStepsForShortestPaths()
        print("Pathfinder time: ", int(round(time.time() * 1000)) - start)
        self.systems[AiMovementSystem.NAME].register(pf)
        self.elements.append(pf)