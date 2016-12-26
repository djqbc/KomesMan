class MovementArtifact:
    NAME = "MovementArtifact"
    def __init__(self, speedModifier=1.0):
        self.speedModifier = speedModifier
        self.movementVector = [0, 0]