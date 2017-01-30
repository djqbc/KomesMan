"""
Menu artifact
"""
class MenuArtifact:
    """
    Container class for bahavior artifact of certain object
    """
    NAME = "MenuArtifact"

    def __init__(self, _action=None):
        """
        Constructor
        :param _action: action which should be performed on menu choice.
        """
        self.action = _action
