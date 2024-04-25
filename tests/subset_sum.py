import unittest
from .utils import describe_test
from src.algorithm.knapsack.subset_sum import SubSet

class TestSubSet_Sum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Subset Sum")

    def test_solve_LLL(self):
        print()
        set = SubSet([17,6,12,14,24], 42)
        X = set.solve_LLL()
        print(X)
        assert(True)
    
    def test_solve_dynamic_prog(self):
        assert(SubSet([17,6,12,14,24]).solve_dynamic_prog() == (23,[17,6]))
        assert(SubSet([23603, 6105, 5851, 19660, 8398, 8545, 14712, 8554, 374 ,13457, 17831, 18309, 25025, 24879, 3145, 22588, 25765, 6105, 19660], 25765).solve_dynamic_prog() == (25765,[6105,19660]))

if __name__ == '__main__':
    unittest.main()