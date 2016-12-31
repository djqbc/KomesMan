import random

class GeneratedBoard:
    '''Class holding randomly generated board'''

    def get_board_binary(self, _sX=16, _sY=12):
        '''returns representation of randomly generated board'''

        # todo: ja bym tutaj dodal rozmieszczenie itemkow na podlodze, ale moze zle mysle?
        board = [[0 for x in range(_sX)] for y in range(_sY)] 
        
        tmp = [0] * 70 + [1] * 30
        for x in range(_sX):
            for y in range(_sY):
                board[y][x] = random.choice(tmp)
        return board