import unittest
from .utils import describe_test
from src.algorithm.simplexe.simplexe import Simplexe

class TestSimplexe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Simplexe")

    def test_1(self):
        print()
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
        print()
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
        print()
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
        print()
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
