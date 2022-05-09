import json
from CODE.world_creator import worldCell
import CODE.world_creator.mappings as wc
import CODE.InputOutput as b

class World:
    __world_size: list
    __world_cells: dict

    def viableCell(self, cell: tuple) -> bool:
        """Checks if a square is viable, aka inside the map"""
        y_axis, x_axis = self.__world_size
        y_pos, x_pos = cell
        if y_pos >= y_axis or y_pos < 0 or x_pos >= x_axis or x_pos < 0:
            return False
        else:
            return True

    def walkableCell(self, cell: tuple) -> bool:
        if not self.viableCell(cell):
            return False
        mapping = self.readSquare(cell)["mapping"]
        if mapping in wc.NON_WALKABLES:
            return False
        return True

    def readSquare(self, cell_pos: tuple) -> dict:
        """Used to get a single specified square on the map"""
        if not self.viableCell(cell_pos):
            return {}

        return self.__world_cells[cell_pos]


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
        y_, x_ = cell_pos
        returnlist = []
        up = (y_-1, x_)
        down = (y_+1, x_)
        left = (y_, x_-1)
        right = (y_, x_+1)

        if y_ > 0 and self.__world_cells[up]:
            returnlist.append({up: self.__world_cells[up]})
        if y_ < self.__world_size[1] and self.__world_cells[down]:
            returnlist.append({down: self.__world_cells[down]})
        if x_ > 0 and self.__world_cells[left]:
            returnlist.append({left: self.__world_cells[left]})
        if x_ < self.__world_size[0] and self.__world_cells[right]:
            returnlist.append({right: self.__world_cells[right]})

        return returnlist

    
    def getDescriptionPlace(self, cell_pos: tuple) -> str:
        if not self.viableCell(cell_pos):
            return "How did you get here?"
        return self.__world_cells[cell_pos]["description"]["place"]


    def getDescriptionDirection(self, cell_pos: tuple) -> str:
        if not self.viableCell(cell_pos):
            return "You see a wall"
        return self.__world_cells[cell_pos]["description"]["look"]


    def getMap(self, position: tuple) -> str:
        y_axis, x_axis = self.__world_size
        _printer = []
        _i = x_axis
        world = self.__world_cells
        for _cell, value in world.items():
            if world[_cell]["mapping"] != wc.RIM:
                if _cell != position:
                    _printer.append(b.get_print_value(value["mapping"]))
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
            "size": self.__world_size,
            "world": self.__world_cells
            }, indent=4)


    def __init__(self, world: dict):
        self.__world_size = world["world_size"]["size"]
        self.__world_cells = world["world"]


if __name__ == '__main__':
    pass
