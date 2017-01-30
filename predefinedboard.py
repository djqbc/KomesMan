"""PredefiniedBoard module."""

class PredefinedBoard:
    """Class holding default predefined board."""

    @staticmethod
    def get_board_binary():
        """
        Get default board.

        Short handout for editing (Enum values not used for ease of editing)
        EMPTY = 0
        WALL = 1
        CAP = 2
        BEER = 3
        DRUG = 4
        PILL = 5
        ENEMY = 6
        KOMESMAN = 7
        TELEPORT = 8
        :return: 2d BoardItems array representing board
        """
        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 2, 2, 2, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 2, 1, 0, 1],
            [1, 2, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0, 1],
            [1, 2, 1, 1, 1, 0, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1],
            [8, 2, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0, 8],
            [1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 6, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
