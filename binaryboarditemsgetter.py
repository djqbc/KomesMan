class BinaryBoardItemsGetter():

    def loadItems(self, board):
        self.caps = []
        self.beers = []
        self.amphs = []
        self.pills = []
        y=0
        for row in board:
            x=0
            for cell in row:
                if cell == 2:
                    self.caps.append((x,y))
                elif cell == 3:
                    self.beers.append((x,y))
                elif cell == 4:
                    self.amphs.append((x,y))
                elif cell == 5:
                    self.pills.append((x,y))
                x += 1
            y += 1