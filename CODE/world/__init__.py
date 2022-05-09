import json
from CODE.world_creator import worldCell
import CODE.world_creator.mappings as wc
import CODE.InputOutput as b

class World:
    world_size: list
    world_cells: dict

    def viableCell(self, cell: tuple) -> bool:
        """Checks if a square is viable, aka inside the map"""
        if cell[0] > self.world_size[0] or cell[0] < 0 or cell[1] > self.world_size[1] or cell[1] < 0:
            return False
        else:
            return True

    def readSquare(self, cell_pos: tuple) -> dict:
        """Used to get a single specified square on the map"""
        if not self.viableCell(cell_pos):
            return {}

        return self.world_cells[str(cell_pos)]


    def getItems(self, cell_pos: tuple) -> dict:
        """Used to get the items from a single specified square"""
        if not self.viableCell(cell_pos):
            return {}

        cell = self.readSquare(cell_pos)
        return cell["items"]


    def getInteractions(self, cell_pos: tuple) -> dict:
        """Used to get the interactions from a single specified square"""
        if not self.viableCell(cell_pos):
            return {}

        cell = self.readSquare(cell_pos)
        return cell["interactions"]


    def getNeighbours(self, cell_pos: tuple) -> list:
        """Used to get the neighbours of a single specified square"""
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


    def getMap(self, position: str) -> str:
        x_axis, y_axis = self.world_size
        _printer = []
        _i = x_axis
        world = self.world_cells
        for _cell in world:
            if world[_cell]["mapping"] != wc.RIM:
                if world[_cell] != world[position]:
                    _printer.append(b.get_print_value(world[_cell]["mapping"]))
                else:
                    _printer.append(b.get_print_value(wc.PLAYER))
            else:
                _printer.append(b.get_print_value(wc.RIM))

        while _i < len(_printer):
            _printer.insert(_i, "\n")  # Adds linebreaks where needed.
            _i += x_axis + 1

        return "{}".format(''.join(_printer))


    def __str__(self):
        return json.dumps({
            "size": self.world_size,
            "world": self.world_cells
            }, indent=4)


    def __init__(self, world: dict):
        self.world_size = world["world_size"]["size"]
        self.world_cells = world["world"]


if __name__ == '__main__':
    pass
