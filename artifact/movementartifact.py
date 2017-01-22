class MovementArtifact:
    NAME = "MovementArtifact"
    baseSpeed = 100

    def __init__(self, speedmodifier=1.0):
        self.speedModifier = self.baseSpeed * speedmodifier
        self.movementVector = [0, 0]
