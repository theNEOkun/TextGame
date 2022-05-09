import unittest

from CODE.char import Char
from CODE.world import World
from CODE.inventory import Item
import CODE.InputOutput as inout

class TestWorld(unittest.TestCase):

    def getWorld(self):
        world = inout.get_file("test.json")
        return World(world)

    def test_cell_viability(self):
        world = self.getWorld()
        self.assertTrue(world.viableCell((0, 0)))
        self.assertFalse(world.viableCell((0, -1)))
        self.assertTrue(world.viableCell((1, 1)))
        self.assertFalse(world.viableCell((0, 4)))

    def test_walkable_cell(self):
        world = self.getWorld()
        self.assertTrue(world.walkableCell((0, 0)))
        self.assertTrue(world.walkableCell((1, 1)))
        self.assertFalse(world.walkableCell((2, 2)))

    def test_read_square(self):
        world = self.getWorld()
        cell = world.readSquare((0, 0))
        cell_check = {
            "description": {
                "place": "It is grassland",
                "look": "You see grassland"
            },
            "items": {"item1": {"desc": "placeholder",
                            "name": "placeholder",
                            "pickup": "no",
                            "hidden_info": "placeholder",
                            "action": "placeholder"
                            }
			},
            "interactions": {"interact1": {"desc": "placeholder",
                                       "key": "no",
                                       "action": "placeholder",
                                       "happening": "placeholder"}
			},
            "mapping": " "
        }
        self.assertEqual(cell, cell_check)

    def test_get_items(self):
        world = self.getWorld()
        items = world.getItems((0, 1))
        expected_items = None
        self.assertEqual(items, expected_items)
        items = world.getItems((0, 0))
        expected_items = {"item1": {"desc": "placeholder",
                            "name": "placeholder",
                            "pickup": "no",
                            "hidden_info": "placeholder",
                            "action": "placeholder"
                            }}
        self.assertEqual(items, expected_items)
        items = world.getItems((1, 0))
        expected_items = {"item1": {"desc": "placeholder",
                            "name": "placeholder",
                            "pickup": "no",
                            "hidden_info": "placeholder",
                            "action": "placeholder"
                            },
					"item2": {"desc": "placeholder",
                            "name": "placeholder",
                            "pickup": "no",
                            "hidden_info": "placeholder",
                            "action": "placeholder"
                            }

			}
        self.assertEqual(items, expected_items)


    def test_get_interactions(self):
        world = self.getWorld()
        interactions = world.getInteractions((0, 0))
        expected_interacts = {"interact1": {"desc": "placeholder",
                                       "key": "no",
                                       "action": "placeholder",
                                       "happening": "placeholder"}
			}
        self.assertEqual(interactions, expected_interacts)
        interactions = world.getInteractions((0, 1))
        expected_interacts = {"interact1": {"desc": "placeholder",
                                       "key": "no",
                                       "action": "placeholder",
                                       "happening": "placeholder"},
							"interact2": {"desc": "placeholder",
                                       "key": "no",
                                       "action": "placeholder",
                                       "happening": "placeholder"}
			}
        self.assertEqual(interactions, expected_interacts)

    def test_get_neighbours(self):
        world = self.getWorld()
        neigh = world.getNeighbours((0, 0))
        cell_pos = []
        for each in neigh:
            for key in each.keys():
                cell_pos.append(key)

        self.assertEqual(cell_pos, [(0, 1), (1, 0)])

        neigh = world.getNeighbours((1, 1))
        cell_pos = []
        for each in neigh:
            for key in each.keys():
                cell_pos.append(key)

        self.assertEqual(cell_pos, [(1, 0), (1, 2), (0, 1), (2, 1)])


class TestChar(unittest.TestCase):

    def test_add_to_inv(self):
        char = Char()
        item = Item("name", "desc", "hidden_info")
        char.addToInv(item)
        self.assertTrue(char.checkInv(item))
        self.assertEqual(item, char.getItemFromInv(item))
        char.remFromInv(item)
        self.assertFalse(char.checkInv(item))


    def test_char_pos(self):
        pos = (0, 0)
        char = Char()
        self.assertEqual(pos, char.getPos())
        char.setPos((1, 0))
        self.assertEqual((1, 0), char.getPos())


    def test_walk(self):
        char = Char()
        char.walk(1, 0)
        self.assertEqual((1, 0), char.getPos())
        char.walk(0, 1)
        self.assertEqual((1, 1), char.getPos())
        char.walk(0, -1)
        self.assertEqual((1, 0), char.getPos())
        char.walk(-1, 0)
        self.assertEqual((0, 0), char.getPos())


class TestMain(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()
