import unittest
from .utils import describe_test
from src.algorithm.simplexe.simplexe import Simplexe

class TestSimplexe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Simplexe")

    def test_something(self):
        canonical_form = [
            [1, 1],
            [1, 0, 2],
            [0, 1, 1],
            [1, 1, 2]
        ]

        simplexe = Simplexe(canonical_form)
        simplexe.print_table()

    def test_something_else(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()
