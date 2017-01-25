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
from myevents import GAME_EVENT, GameEventType, GAME_STATE_CHANGE_EVENT
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
        self.tile_size = 32  

    def build(self, _restart=False):
        resolution_x, resolution_y = (1024, 768)
        self.systems[CollisionSystem.NAME].tile_size = self.tile_size
        
        if not _restart:
            if self.systems[PlayerProgressSystem.NAME].currentLevel == 0:
                self.binaryboard = PredefinedBoard().get_board_binary()
            else:
                self.binaryboard = GeneratedBoard().get_board_binary(resolution_x // self.tile_size, resolution_y // self.tile_size)
            self.createboard(BinaryBoardToSpritesConverter().convert(self.binaryboard), False)
        else:
            self.createboard(BinaryBoardToSpritesConverter().convert(self.binaryboard), True)
            
        itemsgetter = BinaryBoardItemsGetter()
        itemsgetter.load_items(self.binaryboard)

        pygame.event.post(
            pygame.event.Event(GAME_EVENT, reason=GameEventType.SET_MAX_POINTS, maxPoints=len(itemsgetter.caps)))


        for pill in itemsgetter.pills:
            self.createpill(pill[0] * self.tile_size, pill[1] * self.tile_size)
        for cap in itemsgetter.caps:
            self.createcap(cap[0] * self.tile_size, cap[1] * self.tile_size)
        for amph in itemsgetter.amphs:
            self.createdrug(amph[0] * self.tile_size, amph[1] * self.tile_size)
        for beer in itemsgetter.beers:
            self.createbeer(beer[0] * self.tile_size, beer[1] * self.tile_size)
        for enemy in itemsgetter.enemies:
            self.createcop(enemy[0] * self.tile_size, enemy[1] * self.tile_size)
        self.createkomesman(itemsgetter.komesman[0] * self.tile_size, itemsgetter.komesman[1] * self.tile_size)
        for teleport in itemsgetter.teleports:
            self.createteleport(teleport[0] * self.tile_size, teleport[1] * self.tile_size)

        pygame.event.post(pygame.event.Event(GAME_STATE_CHANGE_EVENT, state=GameState.GAME))

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
            elif _event.action == MenuEventType.CHANGE_TILE_SIZE:
                if self.tile_size == 128:
                    self.tile_size = 16
                else:
                    self.tile_size *= 2
        elif _event.type == GAME_EVENT:
            if _event.reason == GameEventType.REMOVE_OBJECT:
                try:
                    self.elements.remove(_event.reference)
                    for _, system in self.systems.items():
                        system.remove(_event.reference)
                except:
                    pass
            elif _event.reason == GameEventType.SPAWN_OBJECT:
                if _event.spawntype == TagType.ENEMY and _event.spawnsubtype == TagSubType.SUPER_COP:
                    self.createsupercop(_event.x, _event.y)
                elif _event.spawntype == TagType.ITEM and _event.spawnsubtype == TagSubType.BAIT:
                    self.createbait(_event.x, _event.y)

    def createkomesman(self, x, y):
        komes_man = Entity()
        komes_man.addartifact(SpriteArtifact(KomesManSprite(self.tile_size), x, y, GameState.GAME))
        komes_man.addartifact(MovementArtifact())
        komes_man.addartifact(TagArtifact(TagType.KOMESMAN))
        komes_man.addartifact(BehaviorArtifact(KomesManBehavior()))
        self.systems[TagSystem.NAME].register(komes_man)
        self.systems[UserMovementSystem.NAME].register(komes_man)
        self.systems[DrawSystem.NAME].register(komes_man)
        self.systems[CollisionSystem.NAME].register(komes_man)
        self.elements.append(komes_man)

    def createcop(self, _x, _y):
        cop = Entity()
        cop.addartifact(SpriteArtifact(CopSprite(self.tile_size), _x, _y, GameState.GAME))
        cop.addartifact(MovementArtifact(1))
        cop.addartifact(TagArtifact(TagType.ENEMY, TagSubType.SIMPLE_COP))
        cop.addartifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)

    def createsupercop(self, _x, _y):
        cop = Entity()
        cop.addartifact(SpriteArtifact(CopSprite(self.tile_size), _x, _y, GameState.GAME))
        cop.addartifact(MovementArtifact(1.5))
        cop.addartifact(TagArtifact(TagType.ENEMY, TagSubType.SUPER_COP))
        cop.addartifact(BehaviorArtifact(SimpleCopBehavior()))
        self.systems[AiMovementSystem.NAME].register(cop)
        self.systems[DrawSystem.NAME].register(cop)
        self.systems[TagSystem.NAME].register(cop)
        self.systems[CollisionSystem.NAME].register(cop)
        self.elements.append(cop)

    def createbeer(self, _x, _y):
        beer = Entity()
        beer.addartifact(SpriteArtifact(BeerSprite(self.tile_size), _x, _y, GameState.GAME))
        beer.addartifact(TagArtifact(TagType.ITEM, TagSubType.BEER))
        beer.addartifact(BehaviorArtifact(BeerBehavior()))
        self.systems[DrawSystem.NAME].register(beer)
        self.systems[TagSystem.NAME].register(beer)
        self.systems[CollisionSystem.NAME].register(beer)
        self.elements.append(beer)

    def createbait(self, _x, _y):
        bait = Entity()
        bait.addartifact(SpriteArtifact(BaitSprite(self.tile_size), _x, _y, GameState.GAME))
        bait.addartifact(TagArtifact(TagType.ITEM, TagSubType.BAIT))
        bait.addartifact(BehaviorArtifact(BaitBehavior()))
        self.systems[DrawSystem.NAME].register(bait)
        self.systems[TagSystem.NAME].register(bait)
        self.systems[CollisionSystem.NAME].register(bait)
        self.elements.append(bait)

    def createdrug(self, _x, _y):
        drug = Entity()
        drug.addartifact(SpriteArtifact(DrugSprite(self.tile_size), _x, _y, GameState.GAME))
        drug.addartifact(TagArtifact(TagType.ITEM, TagSubType.DRUG))
        drug.addartifact(BehaviorArtifact(DrugBehavior()))
        self.systems[DrawSystem.NAME].register(drug)
        self.systems[TagSystem.NAME].register(drug)
        self.systems[CollisionSystem.NAME].register(drug)
        self.elements.append(drug)

    def createcap(self, _x, _y):
        cap = Entity()
        cap.addartifact(SpriteArtifact(CapSprite(self.tile_size), _x, _y, GameState.GAME))
        cap.addartifact(TagArtifact(TagType.ITEM, TagSubType.CAP))
        cap.addartifact(BehaviorArtifact(CapBehavior()))
        self.systems[DrawSystem.NAME].register(cap)
        self.systems[TagSystem.NAME].register(cap)
        self.systems[CollisionSystem.NAME].register(cap)
        self.elements.append(cap)

    def createteleport(self, _x, _y):
        teleport = Entity()
        teleport.addartifact(SpriteArtifact(DummySprite(self.tile_size), _x, _y, GameState.GAME))
        teleport.addartifact(TagArtifact(TagType.FIXED, TagSubType.TELEPORT))
        teleport.addartifact(BehaviorArtifact(TeleportBehavior()))
        self.systems[DrawSystem.NAME].register(teleport)
        self.systems[TagSystem.NAME].register(teleport)
        self.systems[CollisionSystem.NAME].register(teleport)
        self.elements.append(teleport)

    def createpill(self, _x, _y):
        pill = Entity()
        pill.addartifact(SpriteArtifact(PillSprite(self.tile_size), _x, _y, GameState.GAME))
        pill.addartifact(TagArtifact(TagType.ITEM, TagSubType.PILL))
        pill.addartifact(BehaviorArtifact(PillBehavior()))
        self.systems[DrawSystem.NAME].register(pill)
        self.systems[TagSystem.NAME].register(pill)
        self.systems[CollisionSystem.NAME].register(pill)
        self.elements.append(pill)

    def createboard(self, predefinedboard, uselastdata):
        # kijowe bezposrednie przekazanie elements - mozna olac jak nikomu sie nie bedzie chcialo poprawic
        Board(predefinedboard, self.systems, self.elements, self.tile_size)
        start = int(round(time.time() * 1000))
        if uselastdata == False:
            self.lastData = Pathfinder(predefinedboard)
            self.lastData.prepareallstepsforshortestpaths()
            print("Pathfinder time: ", int(round(time.time() * 1000)) - start)
        self.systems[AiMovementSystem.NAME].register(self.lastData)
        self.elements.append(self.lastData)
