
class Item(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc


class Inventory(object):
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.name] = item

    def is_in_inventory(self, item):
        if item in self.items:
            return True
        else:
            return False

    def __str__(self):
        out = '\t'.join(['Name', 'Description'])
        for item in self.items.values():
            out += '\n' + '\t'.join([str(x) for x in [item.name, item.desc]])
        return out
