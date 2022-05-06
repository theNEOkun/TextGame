import CODE.world.World
import CODE.char.Char

class Interacter:
    def open_door(self, door_square: tuple, dirr: string, key_item: Item):
        """This handles the opening of doors"""

        door_interact = curr_square["neighbours"][dirr]

        def updater_door(incoming_order):
            for each in incoming_order:
                coords, direction = each.split("\n")
                self.world[literal_eval(coords)]["neighbours"][direction]["walk"] = "yes"
                self.world[literal_eval(coords)]["directions"][direction] = "You see an open door"

        if door_square["key_needed"] == "no":
            input_orders = door_interact["if_open"].split("\t")
            updater_door(input_orders)
            _status = "You opened the door"
            return _status
        else:
            if key_item == door_square["key_needed"]:
                input_orders = door_interact["if_open"].split("\t")
                updater_door(input_orders)
                _status = "You opened the door with the {}".format(key_item)
                return _status
            else:
                _status = "That's the wrong key"
                return _status


    def chest_opener(self, inventory: Inventory, incoming_interactions):
        if incoming_interactions["happening"]:
            incoming_interactions["desc"] = "the {} seems {}ed".format(interactive_item, action)
            chest_items = incoming_interactions["happening"].split("\t")
            for things in chest_items:
                name, desc, hidden = things.split("\n")
                inventory_chest_adder.add_item(items.Item(name,
                                                          desc,
                                                          hidden))
            return "You opened the chest and got some items"
        else:
            return "There's nothing in the chest"


    def opener(self, key_item_name: string, interactive_item_name: string):
        interactions = self.world.get_interaction(interactive_item)
        if interactive_item_name == "chest":
            if action in interactions["action"]:
                if interactions["key"] != "no":
                    if key_item == interactions["key"]:
                        _status = self.chest_opener(inventory, interactions)
                    else:
                        _status = "That's the wrong item"
                else:
                    _status = self.chest_opener(inventory, interactions)


    def interact(self, interaction: string):
        if "door" in in_put:
            if "the" in in_put:
                nyckel = " ".join(inputs[-2:])
                direction = inputs[4]
                door = self.world[tuple(square["neighbours"][direction]["coord"])]
                _status = self.open_door(door, direction, nyckel)
            else:
                nyckel = " ".join(inputs[-2:])
                direction = inputs[3]
                door = self.world[tuple(square["neighbours"][direction]["coord"])]
                _status = self.open_door(door, direction, nyckel)
        else:
            if "interact" in in_put:
                input_item = " ".join(inputs[2:])
            else:
                input_item = inputs[1]
            _status = interacter(inputs[0], " ".join(inputs[3:]), input_item)


    def pull(self):
        pass


    def touch(self):
        pass


    def mainer(self, action: string, key_item_name: string, interactive_item_name: string):
        """This handles everything regarding interactions with things in the world"""
        try:
            sleep(2)
            _status = ""

            if action == "open":
                self.opener()
            if action == "interact":
                interactions = self.world.get_interaction(interactive_item)
                if self.char.is_in_inventory(interactions["key"]):
                    if action in interactions["action"]:
                        _status = interactions["happening"]
                else:
                    _status = "You need a specific item to do that"
            if action == "pull":
                self.pull()
            if action == "touch":
                self.touch()
        except KeyError:
            _status = "You can't {} that {}".format(action, interactive_item)

        return _status


    def __init__(self, world: World, char: Char):
        self.world = world
        self.char = char


if __name__ == '__main__':
    pass
