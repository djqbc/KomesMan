from sprite.wallsprite import WallKind


class PredefinedBoard:
    '''Class holding default predefined board'''
    def get_board(self):
        '''returns representation of default board'''
        return [
            [WallKind.CORNER_TOPLEFT,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.CORNER_BOTTOMRIGHT],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.HORIZONTAL_WALL,0,0,0,0,0,0,0,0,0,0,0,0,0,0,WallKind.HORIZONTAL_WALL],
            [WallKind.CORNER_TOPLEFT,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.HORIZONTAL_WALL,WallKind.CORNER_BOTTOMRIGHT],
        ]