from inventory import Inventory


class Char:

    pos: tuple
    inventory: Inventory

    def addToInv(self):
        pass

    def remFromInv(self):
        pass

    def setPos(self, pos: tuple):
        self.pos = pos

    def getPos(self) -> tuple:
        return self.pos


    def __init__(self, pos: tuple = (0, 0)):
        self.pos = pos


if __name__ == '__main__':
    pass
