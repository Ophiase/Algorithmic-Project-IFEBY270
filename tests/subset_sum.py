import unittest
from .utils import describe_test
from src.algorithm.knapsack.Subset_sum import SubSet

class TestSubSet_Sum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Subset Sum")

    def test_LLL(self):
        assert(True)
    
    def test_dynamic_prog(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()