from sprite.wallsprite import WallKind


class PredefinedBoard:
    '''Class holding default predefined board'''
    def get_board(self):
        '''returns representation of default board'''
        return [
            [WallKind.CORNER_TOPLEFT,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.CORNER_TOPRIGHT],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.VERTICAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.VERTICAL_WALL],
            [WallKind.CORNER_BOTTOMLEFT,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.CORNER_BOTTOMRIGHT],
        ]

    def get_board_binary(self):
        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]