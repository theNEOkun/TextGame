import CODE.Items
import CODE.Inventory
import CODE.pos as Position


class char:
    inventory: Inventory
    position: tuple


    def take_from_inv(self, item: Item) -> Item:
        self.inventory


    def add_to_inv(self, item: Item):
        self.inventory.ass_item(item)


    def is_in_inventory(self, item: Item) -> bool:
        return self.inventory.is_in_inventory(item)


    def __init__(self, inventory: Inventory):
        self.inventory = inventory

