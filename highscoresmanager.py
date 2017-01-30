"""
HighscoreManager module
"""
import os


class Highscore:
    """
    Class representing one value of highscores
    """
    delimiter = '|'

    def __init__(self, line, score):
        """
        Constructor
        :param line: User name, or line from loaded file if no score specified
        :param score: Score (optional)
        """
        if score is None:
            splitted = line.split(self.delimiter)
            self.name = splitted[0].replace(self.delimiter, '')
            self.score = int(splitted[1])
        else:
            self.name = line
            self.score = score

    def __repr__(self):
        return '{}{}{}'.format(self.name, self.delimiter, self.score)

    def __str__(self):
        return self.__repr__()


class HighscoresManager:
    """
    Class responsible for loading, saving and inserting highscores.
    """
    filename = "highscores.txt"
    topscorescount = 10

    def __init__(self):
        self.highscores = []
        self.loaded = False

    def ishighscore(self, potentialhighscore):
        """
        Function for checking if score is one of best.
        :param potentialhighscore: user score
        :return: True if value is one of best scores, false otherwise.
        """
        if len([x for x in self.highscores if potentialhighscore > x.score]) > 0 or len(
                self.highscores) < self.topscorescount:
            return True
        return False

    def inserthighscore(self, player, score):
        """
        Inserts highscore into internal highscores representation
        :param player: player name as string
        :param score: score as integer
        :return: nothing
        """
        highscore = Highscore(player, score)
        self.highscores.append(highscore)
        self.highscores.sort(key=lambda x: x.score, reverse=True)
        if len(self.highscores) > self.topscorescount:
            self.highscores = self.highscores[:self.topscorescount]

    def load(self):
        """
        Loads highscores from file, for further use.
        :return: nothing
        """
        if not self.loaded:
            if os.path.isfile(self.filename):
                with open(self.filename) as file:
                    for line in file:
                        self.highscores.append(Highscore(line.strip(), None))
        self.loaded = True

    def save(self):
        """
        Saves internal model of highscores to file
        :return: nothing
        """
        with open(self.filename, 'w') as file:
            for highscore in self.highscores:
                file.write(str(highscore))
                file.write('\n')
