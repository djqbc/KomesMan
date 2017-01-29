from board import BoardElement


class BinaryBoardItemsGetter:
    """
    Class responsible for converting items from 2d array into
    lists of coordinates (by map tile)
    """
    def __init__(self):
        """
        Constructor
        """
        self.caps = []
        self.beers = []
        self.amphs = []
        self.pills = []
        self.enemies = []
        self.teleports = []
        self.komesman = (0, 0)

    def load_items(self, board):
        """
        Load items from board into lists of items
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
        y = 0
        for row in board:
            x = 0
            for cell in row:
                if cell == BoardElement.CAP:
                    self.caps.append((x, y))
                elif cell == BoardElement.BEER:
                    self.beers.append((x, y))
                elif cell == BoardElement.DRUG:
                    self.amphs.append((x, y))
                elif cell == BoardElement.PILL:
                    self.pills.append((x, y))
                elif cell == BoardElement.ENEMY:
                    self.enemies.append((x, y))
                elif cell == BoardElement.KOMESMAN:
                    self.komesman = (x, y)
                elif cell == BoardElement.TELEPORT:
                    self.teleports.append((x, y))
                x += 1
            y += 1
