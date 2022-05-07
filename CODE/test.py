import unittest

from char import Char
from world import World
from inventory import Item

class TestWorld(unittest.TestCase):

    def test_assert_true(self):
        self.assertTrue(True)

    def test_read_square(self):
        pass

    def test_get_neighbours(self):
        pass

class TestChar(unittest.TestCase):

    def test_assert_true(self):
        self.assertTrue(True)


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



if __name__ == '__main__':
    unittest.main()
