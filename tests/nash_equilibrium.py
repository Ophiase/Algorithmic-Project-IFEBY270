import unittest
from .utils import describe_test
from src.algorithm.nash_equilibrium.nash_equilibrium import NashEquilibrium

class NashEquilibrium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Nash Equilibrium")

    def test_something(self):
        assert(True)

    def test_something_else(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()
