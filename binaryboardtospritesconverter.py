"""BinaryBoardToSpriteConverter module."""
from sprite.wallsprite import WallKind


class BinaryBoardToSpritesConverter:
    """
    Class designed for converting walls from "binary" representation.

    Creates board walls WallKinds enum values - needed to make better looking corners.
    """

    @staticmethod
    def convert(board):
        """
        Convert array representing board into array representing kinds of walls.

        :param board: 2d array of integers representing map
        :return: 2d array of WallKinds, or 0 in places where is no wall.
        """
        max_y = len(board)
        max_x = len(board[1])

        new_board = []
        tmp_y = 0
        for row in board:
            tmp_x = 0
            new_row = []
            for cell in row:
                if cell == 1:
                    if (tmp_x == 0 and tmp_y == 0 and board[tmp_y][tmp_x + 1] == 1 and board[tmp_y + 1][tmp_x] == 1) \
                            or (tmp_x == 0 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y][tmp_x + 1] == 1 and
                                        board[tmp_y + 1][tmp_x] == 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y][tmp_x - 1] != 1 and
                                        board[tmp_y][tmp_x + 1] == 1 and board[tmp_y + 1][tmp_x] == 1):
                        new_row.append(WallKind.CORNER_TOPLEFT)
                    elif (tmp_x == 0 and tmp_y == 0 and board[tmp_y + 1][tmp_x] != 1 and board[tmp_y][tmp_x + 1] == 1) \
                            or (tmp_x == 0 and tmp_y < max_y - 1 and board[tmp_y + 1][tmp_x] != 1 and board[tmp_y][tmp_x + 1] == 1 and
                                        board[tmp_y - 1][tmp_x] != 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y + 1][tmp_x] != 1 and board[tmp_y][tmp_x + 1] == 1 and
                                        board[tmp_y - 1][tmp_x] != 1 and board[tmp_y][tmp_x - 1] != 1):
                        new_row.append(WallKind.END_LEFT)
                    elif (tmp_y == 0 and tmp_x < max_x - 1 and board[tmp_y][tmp_x - 1] == 1 and board[tmp_y][tmp_x + 1] == 1 and board[tmp_y + 1][
                        tmp_x] != 1) \
                            or (tmp_y == max_y - 1 and tmp_x < max_x - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y][tmp_x - 1] == 1 and
                                        board[tmp_y][tmp_x + 1] == 1) \
                            or (tmp_y < max_y - 1 and tmp_x < max_x - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y][tmp_x - 1] == 1 and
                                        board[tmp_y][tmp_x + 1] == 1 and board[tmp_y + 1][tmp_x] != 1):
                        new_row.append(WallKind.HORIZONTAL_WALL)
                    elif (tmp_x == 0 and tmp_y < max_y - 1 and board[tmp_y][tmp_x + 1] != 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y + 1][
                        tmp_x] == 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y][tmp_x + 1] != 1 and board[tmp_y - 1][tmp_x] == 1 and
                                        board[tmp_y + 1][tmp_x] == 1 and board[tmp_y][tmp_x - 1] != 1) \
                            or (tmp_x == max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y + 1][tmp_x] == 1 and
                                        board[tmp_y][tmp_x - 1] != 1):
                        new_row.append(WallKind.VERTICAL_WALL)
                    elif (tmp_x == 0 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y + 1][tmp_x] != 1 and board[tmp_y][
                            tmp_x + 1] != 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y + 1][tmp_x] != 1 and
                                        board[tmp_y][tmp_x + 1] != 1 and board[tmp_y][tmp_x - 1] != 1) \
                            or (tmp_x == max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y + 1][tmp_x] != 1 and
                                        board[tmp_y][tmp_x - 1] != 1):
                        new_row.append(WallKind.END_BOTTOM)
                    elif tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y + 1][tmp_x] != 1 and board[tmp_y][
                                tmp_x + 1] != 1 and board[tmp_y][tmp_x - 1] == 1:
                        new_row.append(WallKind.END_RIGHT)
                    elif (tmp_x == 0 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y + 1][tmp_x] == 1 and board[tmp_y][
                            tmp_x + 1] != 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y + 1][tmp_x] == 1 and
                                        board[tmp_y][tmp_x + 1] != 1 and board[tmp_y][tmp_x - 1] != 1) \
                            or (tmp_x == max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] != 1 and board[tmp_y + 1][tmp_x] == 1 and
                                        board[tmp_y][tmp_x - 1] != 1):
                        new_row.append(WallKind.END_TOP)
                    elif (tmp_x == 0 and tmp_y == max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y][tmp_x + 1] == 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y][tmp_x + 1] == 1 and
                                        board[tmp_y + 1][tmp_x] != 1 and board[tmp_y][tmp_x - 1] != 1):
                        new_row.append(WallKind.CORNER_BOTTOMLEFT)
                    elif (tmp_x == max_x - 1 and tmp_y == 0 and board[tmp_y][tmp_x - 1] == 1 and board[tmp_y + 1][tmp_x] == 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y][tmp_x - 1] == 1 and board[tmp_y + 1][tmp_x] == 1 and
                                        board[tmp_y - 1][tmp_x] != 1 and board[tmp_y][tmp_x + 1] != 1):
                        new_row.append(WallKind.CORNER_TOPRIGHT)
                    elif (tmp_x == max_x - 1 and tmp_y == max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y][tmp_x - 1] == 1) \
                            or (tmp_x < max_x - 1 and tmp_y < max_y - 1 and board[tmp_y - 1][tmp_x] == 1 and board[tmp_y][tmp_x - 1] == 1 and
                                        board[tmp_y][tmp_x + 1] != 1 and board[tmp_y + 1][tmp_x] != 1):
                        new_row.append(WallKind.CORNER_BOTTOMRIGHT)
                    elif (tmp_x > 0 and tmp_y > 0 and tmp_x < max_x - 1 and tmp_y < max_y - 1) and board[tmp_y-1][tmp_x] == 1 and board[tmp_y-1][tmp_x-1] == 1 \
                            and board[tmp_y - 1][tmp_x+1] == 1 and board[tmp_y][tmp_x-1] == 1 and board[tmp_y][tmp_x+1] == 1 and board[tmp_y+1][tmp_x] == 1 \
                            and board[tmp_y + 1][tmp_x-1] == 1 and board[tmp_y+1][tmp_x+1] == 1:
                        new_row.append(WallKind.BLANK)
                    else:
                        new_row.append(WallKind.SQUARE)
                else:
                    new_row.append(0)
                tmp_x += 1
            tmp_y += 1
            new_board.append(new_row)
        return new_board
