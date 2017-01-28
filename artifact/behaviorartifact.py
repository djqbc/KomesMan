class BehaviorArtifact:
    """
    Container class for bahavior artifact of certain object
    """
    NAME = "BehaviorArtifact"

    def __init__(self, _behavior=None):
        """
        Constructor
        :param _behavior: behavior of certain object
        """
        self.behavior = _behavior
