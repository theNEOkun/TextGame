class Item(object):
    def __init__(self, name, desc, hidden_info):
        self.name = name
        self.desc = desc
        self.hidden_info = hidden_info


class Inventory(object):
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.name] = item

    def is_in_inventory(self, item):
        if self.items:
            if item in self.items:
                return True
            else:
                return False

    def hidden_info(self, input_item):
        item_status = False
        for item in self.items.values():
            if item.hidden_info == input_item:
                item_status = True
        return item_status

    def saveer(self):
        out_save = '\t'.join(['Name', 'Description', 'Hidden_info'])
        for item in self.items.values():
            out_save += '\n' + '\t'.join([str(x) for x in [item.name, item.desc, item.hidden_info]])
        return out_save

    def __str__(self):
        out = '\t'.join(['Name', 'Description'])
        for item in self.items.values():
            out += '\n' + '\t'.join([str(x) for x in [item.name, item.desc]])
        return out
