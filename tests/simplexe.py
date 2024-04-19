import unittest
from .utils import describe_test
from src.algorithm.simplexe.simplexe import Simplexe

class TestSimplexe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Simplexe")

    def test_1(self):
        print("\033[92mExpected Optimal Solution for Test 1: [8.0, 4.0, 0, 18.0, 0, 0]\033[0m")
        canonical_form = [
            [3, 1, 2],
            [1, 1, 3, 30],
            [2, 2, 5, 24],
            [4, 1, 2, 36]
        ]

        simplexe = Simplexe(canonical_form)
        simplexe.execute_simplexe()
        simplexe.print_all()

    def test_2(self):
        print("\033[92mExpected Optimal Solution for Test 2: [2.0, 0.0, 0, 1.0, 0]\033[0m")
        canonical_form = [
            [1, 1],
            [1, 0, 2],
            [0, 1, 1],
            [1, 1, 2]
        ]

        simplexe = Simplexe(canonical_form)
        simplexe.execute_simplexe()
        simplexe.print_all()

    def test_3(self):
        print("\033[92mExpected Optimal Solution for Test 3: [626.086956521739, 334.7826086956522, 0, 0, 486.9565217391296]\033[0m")
        canonical_form = [
            [900, 1000],
            [11, 9, 9900],
            [7, 12, 8400],
            [6, 16, 9600]
        ]
        simplexe = Simplexe(canonical_form)
        simplexe.execute_simplexe()
        simplexe.print_all()

    def test_unbounded(self):
        print("\033[92mExpected Optimal Solution for Test Unbounded: [0, 0, 3, 5]\033[0m")
        canonical_form = [
            [1, 2],
            [-1, -1, 3],
            [2, 3, 5],
        ]

        simplexe = Simplexe(canonical_form)
        simplexe.execute_simplexe()
        simplexe.print_all()

if __name__ == '__main__':
    unittest.main()