"""Binary Board Item Getter."""
from board import BoardElement


class BinaryBoardItemsGetter:
    """
    Class responsible for converting items from 2d array.

    Creates lists of coordinates (by map tile)
    """

    def __init__(self):
        """Constructor."""
        self.caps = []
        self.beers = []
        self.amphs = []
        self.pills = []
        self.enemies = []
        self.teleports = []
        self.komesman = (0, 0)

    def load_items(self, board):
        """
        Load items from board into lists of items.

        :param board: board to process
        :return: nothing
        """
        self.caps.clear()
        self.beers.clear()
        self.amphs.clear()
        self.pills.clear()
        self.enemies.clear()
        self.teleports.clear()
        self.komesman = (0, 0)
        tmp_y = 0
        for row in board:
            tmp_x = 0
            for cell in row:
                if cell == BoardElement.CAP:
                    self.caps.append((tmp_x, tmp_y))
                elif cell == BoardElement.BEER:
                    self.beers.append((tmp_x, tmp_y))
                elif cell == BoardElement.DRUG:
                    self.amphs.append((tmp_x, tmp_y))
                elif cell == BoardElement.PILL:
                    self.pills.append((tmp_x, tmp_y))
                elif cell == BoardElement.ENEMY:
                    self.enemies.append((tmp_x, tmp_y))
                elif cell == BoardElement.KOMESMAN:
                    self.komesman = (tmp_x, tmp_y)
                elif cell == BoardElement.TELEPORT:
                    self.teleports.append((tmp_x, tmp_y))
                tmp_x += 1
            tmp_y += 1
