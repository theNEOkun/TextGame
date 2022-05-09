from CODE.inventory import Inventory
from CODE.inventory import Item

from CODE.char.directions import Directions as Dir

class Char(object):

    char_x: int
    char_y: int
    inventory: Inventory
    step_size: int = 1

    def addToInv(self, item: Item):
        """Adds to char inventory"""
        self.inventory.add_item(item)


    def remFromInv(self, item: Item) -> Item:
        """Remove from char inventory"""
        self.inventory.remove_item(item)


    def getItemFromInv(self, item: Item) -> Item:
        """Fetches from char inventory"""
        return self.inventory.get_item(item)


    def checkInv(self, item: Item) -> bool:
        """Checks if item is in inventory"""
        return self.inventory.is_in_inventory(item)


    def walk(self, direction: Dir):
        """
        Used to walk a char
        :param ew > 0 = walk east, < 0 = walk west
        :param ns > 0 = walk north, < 0 = walk south
        """
        if direction == Dir.UP:
            self.char_y -= self.step_size
        elif direction == Dir.DOWN:
            self.char_y += self.step_size
        elif direction == Dir.LEFT:
            self.char_x -= self.step_size
        elif direction == Dir.RIGHT:
            self.char_x += self.step_size


    def setPos(self, pos: tuple):
        """Set position of char"""
        self.char_x = pos[1]
        self.char_y = pos[0]


    def getPos(self) -> tuple:
        """Get position of char"""
        return (self.char_y, self.char_x)


    def __str__(self) -> str:
        return "Name: {}\nInv: {}".format(self.name, self.inventory)


    def __init__(self, pos: tuple = (0, 0)):
        self.setPos(pos)
        self.inventory = Inventory()


    def __init__(self, name: str = "Steve", inv: Inventory = Inventory(), pos: tuple = (0, 0)):
        self.name = name
        self.inventory = inv
        self.setPos(pos)


if __name__ == '__main__':
    pass
