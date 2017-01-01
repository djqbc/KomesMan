class PredefinedBoard:
    '''Class holding default predefined board'''

    def get_board_binary(self):
        '''returns representation of default board'''

        # todo: ja bym tutaj dodal rozmieszczenie itemkow na podlodze, ale moze zle mysle?

#         EMPTY = 0
#         WALL = 1
#         CAP = 2
#         BEER = 3
#         DRUG = 4
#         PILL = 5
#         ENEMY = 6
#         KOMESMAN = 7

        return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 2, 2, 2, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 2, 1, 0, 1],
            [1, 2, 1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 0, 1],
            [1, 2, 1, 1, 1, 0, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1],
            [0, 2, 0, 0, 0, 0, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0],
            [1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 6, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]