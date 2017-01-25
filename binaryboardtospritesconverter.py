from sprite.wallsprite import WallKind


class BinaryBoardToSpritesConverter:
    @staticmethod
    def convert(board):
        max_y = len(board)
        max_x = len(board[1])

        new_board = []
        y = 0
        for row in board:
            x = 0
            new_row = []
            for cell in row:
                if cell == 1:
                    if (x == 0 and y == 0 and board[y][x + 1] == 1 and board[y + 1][x] == 1) \
                            or (x == 0 and y < max_y - 1 and board[y - 1][x] != 1 and board[y][x + 1] == 1 and
                                        board[y + 1][x] == 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y - 1][x] != 1 and board[y][x - 1] != 1 and
                                        board[y][x + 1] == 1 and board[y + 1][x] == 1):
                        new_row.append(WallKind.CORNER_TOPLEFT)
                    elif (x == 0 and y == 0 and board[y + 1][x] != 1 and board[y][x + 1] == 1) \
                            or (x == 0 and y < max_y - 1 and board[y + 1][x] != 1 and board[y][x + 1] == 1 and
                                        board[y - 1][x] != 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y + 1][x] != 1 and board[y][x + 1] == 1 and
                                        board[y - 1][x] != 1 and board[y][x - 1] != 1):
                        new_row.append(WallKind.END_LEFT)
                    elif (y == 0 and x < max_x - 1 and board[y][x - 1] == 1 and board[y][x + 1] == 1 and board[y + 1][
                        x] != 1) \
                            or (y == max_y - 1 and x < max_x - 1 and board[y - 1][x] != 1 and board[y][x - 1] == 1 and
                                        board[y][x + 1] == 1) \
                            or (y < max_y - 1 and x < max_x - 1 and board[y - 1][x] != 1 and board[y][x - 1] == 1 and
                                        board[y][x + 1] == 1 and board[y + 1][x] != 1):
                        new_row.append(WallKind.HORIZONTAL_WALL)
                    elif (x == 0 and y < max_y - 1 and board[y][x + 1] != 1 and board[y - 1][x] == 1 and board[y + 1][
                        x] == 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y][x + 1] != 1 and board[y - 1][x] == 1 and
                                        board[y + 1][x] == 1 and board[y][x - 1] != 1) \
                            or (x == max_x - 1 and y < max_y - 1 and board[y - 1][x] == 1 and board[y + 1][x] == 1 and
                                        board[y][x - 1] != 1):
                        new_row.append(WallKind.VERTICAL_WALL)
                    elif (x == 0 and y < max_y - 1 and board[y - 1][x] == 1 and board[y + 1][x] != 1 and board[y][
                            x + 1] != 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y - 1][x] == 1 and board[y + 1][x] != 1 and
                                        board[y][x + 1] != 1 and board[y][x - 1] != 1) \
                            or (x == max_x - 1 and y < max_y - 1 and board[y - 1][x] == 1 and board[y + 1][x] != 1 and
                                        board[y][x - 1] != 1):
                        new_row.append(WallKind.END_BOTTOM)
                    elif x < max_x - 1 and y < max_y - 1 and board[y - 1][x] != 1 and board[y + 1][x] != 1 and board[y][
                                x + 1] != 1 and board[y][x - 1] == 1:
                        new_row.append(WallKind.END_RIGHT)
                    elif (x == 0 and y < max_y - 1 and board[y - 1][x] != 1 and board[y + 1][x] == 1 and board[y][
                            x + 1] != 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y - 1][x] != 1 and board[y + 1][x] == 1 and
                                        board[y][x + 1] != 1 and board[y][x - 1] != 1) \
                            or (x == max_x - 1 and y < max_y - 1 and board[y - 1][x] != 1 and board[y + 1][x] == 1 and
                                        board[y][x - 1] != 1):
                        new_row.append(WallKind.END_TOP)
                    elif (x == 0 and y == max_y - 1 and board[y - 1][x] == 1 and board[y][x + 1] == 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y - 1][x] == 1 and board[y][x + 1] == 1 and
                                        board[y + 1][x] != 1 and board[y][x - 1] != 1):
                        new_row.append(WallKind.CORNER_BOTTOMLEFT)
                    elif (x == max_x - 1 and y == 0 and board[y][x - 1] == 1 and board[y + 1][x] == 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y][x - 1] == 1 and board[y + 1][x] == 1 and
                                        board[y - 1][x] != 1 and board[y][x + 1] != 1):
                        new_row.append(WallKind.CORNER_TOPRIGHT)
                    elif (x == max_x - 1 and y == max_y - 1 and board[y - 1][x] == 1 and board[y][x - 1] == 1) \
                            or (x < max_x - 1 and y < max_y - 1 and board[y - 1][x] == 1 and board[y][x - 1] == 1 and
                                        board[y][x + 1] != 1 and board[y + 1][x] != 1):
                        new_row.append(WallKind.CORNER_BOTTOMRIGHT)
                    elif (x > 0 and y > 0 and x < max_x - 1 and y < max_y - 1) and board[y-1][x] == 1 and board[y-1][x-1] == 1 \
                            and board[y - 1][x+1] == 1 and board[y][x-1] == 1 and board[y][x+1] == 1 and board[y+1][x] == 1 \
                            and board[y + 1][x-1] == 1 and board[y+1][x+1] == 1:
                        new_row.append(WallKind.BLANK)
                    else:
                        new_row.append(WallKind.SQUARE)
                else:
                    new_row.append(0)
                x += 1
            y += 1
            new_board.append(new_row)
        return new_board
