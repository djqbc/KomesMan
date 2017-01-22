class MovementArtifact:
    NAME = "MovementArtifact"
    baseSpeed = 100

    def __init__(self, speedModifier=1.0):
        self.speedModifier = self.baseSpeed * speedModifier
        self.movementVector = [0, 0]
