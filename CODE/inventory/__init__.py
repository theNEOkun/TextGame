class Item(object):
    def __init__(self, name, desc, hidden_info):
        self.name = name
        self.desc = desc
        self.hidden_info = hidden_info

    def __eq__(self, item):
        if isinstance(item, self.__class__):
            return self.name == item.name
        else:
            return False

    def __ne__(self, item):
        return not self.__eq__(item)


class Inventory(object):
    def __init__(self):
        self.items = {}


    def add_item(self, item: Item):
        """Adds item to inventory"""
        self.items[item.name] = item


    def get_item(self, item: Item):
        """Fetches item from inventory"""
        if self.is_in_inventory(item):
            return self.items[item.name]
        else:
            False


    def remove_item(self, item: Item):
        """Removes item from inventory"""
        if self.is_in_inventory(item):
            del self.items[item.name]
            return True
        else:
            return False


    def is_in_inventory(self, item: Item):
        """Checks if item is in inventory"""
        try:
            if self.items[item.name]:
                return True
            else:
                return False
        except KeyError:
            return False


    def hidden_info(self, secret: str):
        """Checks if some item has a secret"""
        item_status = False
        for item in self.items.values():
            if item.hidden_info == secret:
                item_status = True
        return item_status


    def saveer(self):
        """Used when saving"""
        out_save = '\t'.join(['Name', 'Description', 'Hidden_info'])
        for item in self.items.values():
            out_save += '\n' + '\t'.join([str(x) for x in [item.name, item.desc, item.hidden_info]])
        return out_save


    def __str__(self):
        """Prints inventory to screen"""
        out = '\t'.join(['Name', 'Description'])
        for item in self.items.values():
            out += '\n' + '\t'.join([str(x) for x in [item.name, item.desc]])
        return out
