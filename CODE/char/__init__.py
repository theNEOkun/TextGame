from inventory import Inventory
from inventory import Item


class Char:

    pos: tuple
    inventory: Inventory

    def addToInv(self, item: Item):
        self.inventory.add_item(item)


    def remFromInv(self, item: Item) -> Item:
        self.inventory.remove_item(item)


    def getItemFromInv(self, item: Item) -> Item:
        return self.inventory.get_item(item)


    def checkInv(self, item: Item) -> bool:
        return self.inventory.is_in_inventory(item)


    def setPos(self, pos: tuple):
        self.pos = pos


    def getPos(self) -> tuple:
        return self.pos


    def __init__(self, pos: tuple = (0, 0)):
        self.pos = pos
        self.inventory = Inventory()


if __name__ == '__main__':
    pass
