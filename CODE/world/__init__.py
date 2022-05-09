import json
from CODE.world_creator import worldCell

class World:
    world_size: int
    world_cells: dict

    def readSquare(self):
        pass

    
    def getNeighbours(self, cell_pos: tuple) -> list:
        pass


    def __str__(self):
        return json.dumps({
                "size": self.world_size,
                "world": self.world_cells
                }, indent=4)


    def __init__(self, world_size: list, world_cells: dict):
        self.world_size = world_size
        self.world_cells = world_cells


if __name__ == '__main__':
    pass
