import unittest

from CODE.char import Char
from CODE.char.directions import Directions as Dir
from CODE.world import World
from CODE.inventory import Item
from CODE.game_handler import MainClass
from CODE.game_handler.command import Command
import CODE.InputOutput as inout

import CODE.world_creator as wc

class TestWorld(unittest.TestCase):

    def test_cell_viability(self):
        world = getWorld()
        self.assertTrue(world.viableCell((0, 0)))
        self.assertFalse(world.viableCell((0, -1)))
        self.assertTrue(world.viableCell((1, 1)))
        self.assertFalse(world.viableCell((0, 4)))

    def test_walkable_cell(self):
        world = getWorld()
        self.assertTrue(world.walkableCell((0, 0)))
        self.assertTrue(world.walkableCell((1, 1)))
        self.assertFalse(world.walkableCell((2, 2)))

    def test_read_square(self):
        world = getWorld()
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
        world = getWorld()
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
        world = getWorld()
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
        world = getWorld()
        neigh = world.getNeighbours((0, 0))
        cell_pos = []
        for each in neigh:
            for key in each.keys():
                cell_pos.append(key)

        self.assertEqual(cell_pos, [(1, 0), (0, 1)])

        neigh = world.getNeighbours((1, 1))
        cell_pos = []
        for each in neigh:
            for key in each.keys():
                cell_pos.append(key)

        self.assertEqual(cell_pos, [(0, 1), (2, 1), (1, 0), (1, 2)])


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
        char.walk(Dir.DOWN)
        self.assertEqual((1, 0), char.getPos())
        char.walk(Dir.RIGHT)
        self.assertEqual((1, 1), char.getPos())
        char.walk(Dir.LEFT)
        self.assertEqual((1, 0), char.getPos())
        char.walk(Dir.UP)
        self.assertEqual((0, 0), char.getPos())


class TestMain(unittest.TestCase):
    
    def test_walk_char(self):
        main = getMain()
        self.assertEqual((1, 1), main.char_pos())
        self.assertTrue(main.walk_char(Dir.DOWN))
        self.assertEqual((2, 1), main.char_pos())
        self.assertFalse(main.walk_char(Dir.DOWN))
        self.assertEqual((2, 1), main.char_pos())
        self.assertTrue(main.walk_char(Dir.LEFT))
        self.assertEqual((2, 0), main.char_pos())


    def test_walk_command(self):
        main = getMain()
        self.assertEqual((1, 1), main.char_pos())
        arguments = ["s"]
        main.walk_command(arguments)
        self.assertEqual((2, 1), main.char_pos())
        arguments = ["n"]
        main.walk_command(arguments)
        self.assertEqual((1, 1), main.char_pos())


    def test_options(self):
        main = getMain()
        command = "walk s"
        arg, rest = main.checkCommand(command)
        self.assertEqual(arg, Command.WALK)
        self.assertEqual(rest, ["s"])
        command = "walk n"
        arg, rest = main.checkCommand(command)
        self.assertEqual(arg, Command.WALK)
        self.assertEqual(rest, ["n"])
        command = "look around"
        arg, rest = main.checkCommand(command)
        self.assertEqual(arg, Command.LOOK)
        self.assertEqual(rest, ["around"])
        command = "jump"
        arg, rest = main.checkCommand(command)
        self.assertEqual(arg, None)
        self.assertEqual(rest, None)


    def test_command_flow(self):
        pass


def getWorld():
    world = inout.get_file("test.json")
    return World(world)


def getMain() -> MainClass:
    world = getWorld()
    char = Char(pos=(1, 1))
    return MainClass(world, char)

if __name__ == '__main__':
    unittest.main()
