import unittest

from char import Char
from world import World

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


    def test_char_pos(self):
        pos = (0, 0)
        char = Char(pos)
        self.assertEqual(pos, char.getPos())
        char.setPos((1, 0))
        self.assertEqual((1, 0), char.getPos())



if __name__ == '__main__':
    unittest.main()
