import json
from CODE.world_creator import worldCell

class World:
    world_size: list
    world_cells: dict

    def readSquare(self):
        pass


    def getNeighbours(self, cell_pos: tuple) -> list:
        x_, y_ = cell_pos
        returnlist = []
        up = (x_, y_-1)
        down = (x_, y_+1)
        left = (x_-1, y_)
        right = (x_+1, y_)

        if y_ > 0 and self.world_cells[str(up)]:
            returnlist.append({up: self.world_cells[str(up)]})
        if y_ < self.world_size[1] and self.world_cells[str(down)]:
            returnlist.append({down: self.world_cells[str(down)]})
        if x_ > 0 and self.world_cells[str(left)]:
            returnlist.append({left: self.world_cells[str(left)]})
        if x_ < self.world_size[0] and self.world_cells[str(right)]:
            returnlist.append({right: self.world_cells[str(right)]})

        return returnlist


    def __str__(self):
        return json.dumps({
            "size": self.world_size,
            "world": self.world_cells
            }, indent=4)


    def __init__(self, world_size: list, world_cells: dict):
        self.world_size = world_size["size"]
        self.world_cells = world_cells


if __name__ == '__main__':
    pass
