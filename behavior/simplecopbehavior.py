from myevents import COLLISION_EVENT
from artifact.tagartifact import TagArtifact, TagType
class SimpleCopBehavior:
    def input(self, _event, _postEventCallback):
        if _event.type == COLLISION_EVENT:
            entity = _event.colliding
            if entity.artifacts[TagArtifact.NAME].type == TagType.KOMESMAN:
                #play some demonic laugh
                #_postEventCallback(Event(PLAY_MUSIC, song="hahahaha.mp3"))
                pass