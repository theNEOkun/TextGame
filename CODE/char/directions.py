from enum import IntEnum

class Directions(IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    NOT = 0

    @classmethod
    def get_direction(self, argument):
        if argument == "n" or argument == "north" or argument == "up":
            return self.UP
        elif argument == "s" or argument == "south" or argument == "down":
            return self.DOWN
        elif argument == "w" or argument == "west" or argument == "left":
            return self.LEFT
        elif argument == "e" or argument == "east" or argument == "right":
            return self.RIGHT
