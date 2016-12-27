from sprite.wallsprite import WallKind


class BinaryBoardToSpritesConverter():
    def convert(self, board):
        maxY = len(board)
        maxX = len(board[1])

        newBoard = []
        y=0
        for row in board:
            x=0
            newRow = []
            for cell in row:
                if cell == 1:
                    if (x==0 and y==0 and board[y][x+1] == 1 and board[y+1][x] == 1) \
                            or (x == 0 and y < maxY-1 and board[y-1][x] == 0 and board[y][x+1] == 1 and board[y+1][x] == 1)\
                            or (x < maxX-1 and y< maxY - 1 and board[y-1][x] == 0 and board[y][x-1] == 0 and board[y][x+1] == 1 and board[y+1][x] == 1):
                        newRow.append(WallKind.CORNER_TOPLEFT)
                    elif (x==0 and y==0 and board[y+1][x] == 0 and board[y][x+1] == 1)\
                            or (x == 0 and y < maxY-1 and board[y+1][x] == 0 and board[y][x+1] == 1 and board[y-1][x] == 0)\
                            or (x < maxX-1 and y< maxY - 1 and board[y+1][x] == 0 and board[y][x+1] == 1 and board[y-1][x] == 0 and board[y][x-1] == 0):
                        newRow.append(WallKind.END_LEFT)
                    elif(y==0 and x < maxX-1 and board[y][x-1] == 1 and board[y][x+1] == 1 and board[y+1][x] == 0)\
                            or (y == maxY-1 and x < maxX-1 and board[y-1][x] == 0 and board[y][x-1] == 1 and board[y][x+1] == 1)\
                            or (y < maxY-1 and x < maxX-1 and board[y-1][x] == 0 and board[y][x-1] == 1 and board[y][x+1] == 1 and board[y+1][x] == 0):
                        newRow.append(WallKind.HORIZONTAL_WALL)
                    elif(x==0 and y < maxY-1 and board[y][x+1] == 0 and board[y-1][x] == 1 and board[y+1][x] == 1)\
                            or (x<maxX-1 and y<maxY-1 and board[y][x+1] == 0 and board[y-1][x] == 1 and board[y+1][x] == 1 and board[y][x-1] == 0)\
                            or (x==maxX-1 and y<maxY-1 and board[y-1][x] == 1 and board[y+1][x] == 1 and board[y][x-1] == 0):
                        newRow.append(WallKind.VERTICAL_WALL)
                    elif(x==0 and y < maxY-1 and board[y-1][x] == 1 and board[y+1][x]==0 and board[y][x+1] == 0)\
                            or (x<maxX-1 and y < maxY-1 and board[y-1][x] == 1 and board[y+1][x]==0 and board[y][x+1] == 0  and board[y][x-1] == 0) \
                            or (x==maxX-1 and y<maxY-1 and board[y-1][x] == 1 and board[y+1][x] == 0 and board[y][x - 1] == 0):
                        newRow.append(WallKind.END_BOTTOM)
                    elif(x<maxX-1 and y<maxY-1 and board[y-1][x]==0 and board[y+1][x]==0 and board[y][x+1]==0 and board[y][x-1]==1):
                        newRow.append(WallKind.END_RIGHT)
                    elif(x==0 and y<maxY-1 and board[y-1][x] == 0 and board[y+1][x] == 1 and board[y][x+1] == 0)\
                            or (x < maxX-1 and y<maxY-1 and board[y-1][x] == 0 and board[y+1][x] == 1 and board[y][x+1] == 0 and board[y][x-1] == 0) \
                            or (x == maxX-1 and y<maxY-1 and board[y-1][x] == 0 and board[y+1][x] == 1 and board[y][x-1] == 0)                        :
                        newRow.append(WallKind.END_TOP)
                    elif(x==0 and y == maxY-1 and board[y-1][x] == 1 and board[y][x+1] == 1)\
                            or (x < maxX-1 and y < maxY - 1 and board[y-1][x] == 1 and board[y][x+1] == 1  and board[y+1][x] == 0 and board[y][x-1] == 0):
                        newRow.append(WallKind.CORNER_BOTTOMLEFT)
                    elif(x==maxX-1 and y==0 and board[y][x-1] == 1 and board[y+1][x] == 1)\
                            or(x<maxX-1 and y<maxY-1 and board[y][x-1] == 1 and board[y+1][x] == 1 and board[y-1][x] ==0 and board[y][x+1]==0):
                        newRow.append(WallKind.CORNER_TOPRIGHT)
                    elif(x==maxX-1 and y==maxY-1 and board[y-1][x]==1 and board[y][x-1] ==1)\
                            or (x<maxX-1 and y<maxY-1 and board[y-1][x]==1 and board[y][x-1] ==1 and board[y][x+1] ==0 and board[y+1][x] ==0):
                        newRow.append(WallKind.CORNER_BOTTOMRIGHT)
                    else:
                        newRow.append(WallKind.SQUARE)
                else:
                    newRow.append(0)
                x += 1
            y += 1
            newBoard.append(newRow)
        return newBoard