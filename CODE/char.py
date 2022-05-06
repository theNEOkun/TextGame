import CODE.Items
import CODE.Inventory
import CODE.pos as Position


class char:
    inventory: Inventory
    position: tuple

    def take_from_inv(self, item) -> Item:
        self.inventory


    def is_in_inventory(self, item) -> bool:
        return self.inventory.is_in_inventory(item)


    def __init__(self):
        self.inventory = {}

