import unittest
from entity import Entity
from artifact.tagartifact import TagArtifact, TagType, TagSubType
from system.tagsystem import TagSystem

class TestTagSystem(unittest.TestCase):
    def test_get_by_type(self):
        e = Entity()
        e.addartifact(TagArtifact(TagType.KOMESMAN))
        system = TagSystem()
        system.register(e)
        
        self.assertEqual(len(system.getentities(TagType.KOMESMAN)), 1)
        self.assertEqual(len(system.getentities(TagType.ENEMY)), 0)
    
    def test_get_by_subtype(self):
        e = Entity()
        e.addartifact(TagArtifact(TagType.KOMESMAN, TagSubType.BEER))
        system = TagSystem()
        system.register(e)
        
        self.assertEqual(len(system.getentities(TagType.KOMESMAN)), 1)
        self.assertEqual(len(system.getentities(TagType.KOMESMAN, TagSubType.BAIT)), 0)
        self.assertEqual(len(system.getentities(TagType.KOMESMAN, TagSubType.BEER)), 1)
    
    def test_remove(self):
        e = Entity()
        e.addartifact(TagArtifact(TagType.KOMESMAN, TagSubType.BEER))
        system = TagSystem()
        system.register(e)
        
        self.assertEqual(len(system.getentities(TagType.KOMESMAN)), 1)
        system.remove(e)
        self.assertEqual(len(system.getentities(TagType.KOMESMAN)), 0)