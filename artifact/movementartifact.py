class MovementArtifact:
    """
    Container class for movement properties.
    """
    NAME = "MovementArtifact"
    baseSpeed = 100

    def __init__(self, speedmodifier=1.0):
        """
        Constructor
        :param speedmodifier:  Value which base speed will be multiplied with
        """
        self.speedModifier = self.baseSpeed * speedmodifier
        self.movementVector = [0, 0]
        self.target = None
