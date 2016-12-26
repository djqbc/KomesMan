from artifact.spriteartifact import SpriteArtifact

class DrawSystem:
    observing = []
    def register(self, _object):
        if SpriteArtifact.NAME in _object.artifacts:   
            self.observing.append(_object)
        else:
            raise NameError("ERROR!!!")
    def draw(self, _screen):
        for entity in self.observing:
            entity.artifacts[SpriteArtifact.NAME].sprite.draw(_screen, entity.artifacts[SpriteArtifact.NAME].positionX, 
                                                              entity.artifacts[SpriteArtifact.NAME].positionY)
    def update(self, _timeDelta):
        for entity in self.observing:
            entity.artifacts[SpriteArtifact.NAME].sprite.update(_timeDelta)