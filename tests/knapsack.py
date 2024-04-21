import unittest
from .utils import describe_test
from src.algorithm.knapsack.knapsack import KnapSack

class TestKnapSack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Knap Sack")

    def test_upper_bound(self):
        assert(KnapSack(1,[2,2,2],[2,1,3]).upper_bound() == 1.5)
        assert(KnapSack(4,[1,1,1,2],[3,2,1,1]).upper_bound() == 6.5)
        assert(KnapSack(3,[1,1,1,2],[3,2,1,1]).upper_bound() == 6.0)
        assert(KnapSack(2,[1,1,1,2],[3,2,1,1]).upper_bound() == 5.0)
        assert(KnapSack(2,[3,2,1,1],[3,2,1,1]).upper_bound() == 2.0)
        assert(KnapSack(3,[2,2,2,2],[2,1,1,1]).upper_bound() == 2.5)
        assert(KnapSack(9,[2,2,2,2],[2,1,1,1]).upper_bound() == 5.0)
        assert(KnapSack(9,[5,5,4],[10,10,4]).upper_bound() == 18.0)
        assert(KnapSack(9,[7,5,4],[14,9,7]).upper_bound() == 17.6)

    def test_lower_bound(self):
        assert(KnapSack(1,[2,2,2],[2,1,3]).lower_bound() == 0)
        assert(KnapSack(4,[1,1,1,2],[3,2,1,1]).lower_bound() == 6)
        assert(KnapSack(3,[1,1,1,2],[3,2,1,1]).lower_bound() == 6)
        assert(KnapSack(2,[1,1,1,2],[3,2,1,1]).lower_bound() == 5)
        assert(KnapSack(2,[3,2,1,1],[3,2,1,1]).lower_bound() == 2)
        assert(KnapSack(3,[2,2,2,2],[2,1,1,1]).lower_bound() == 2)
        assert(KnapSack(9,[2,2,2,2],[2,1,1,1]).lower_bound() == 5)
        assert(KnapSack(9,[5,5,4],[10,10,4]).lower_bound() == 14)
        assert(KnapSack(9,[7,5,4],[14,9,7]).lower_bound() == 14)
        
    def test_branch_and_bound(self):
        assert(KnapSack(1,[2,2,2],[2,1,3]).branch_and_bound() == 0)
        assert(KnapSack(4,[1,1,1,2],[3,2,1,1]).branch_and_bound() == 6)
        assert(KnapSack(3,[1,1,1,2],[3,2,1,1]).branch_and_bound() == 6)
        assert(KnapSack(2,[1,1,1,2],[3,2,1,1]).branch_and_bound() == 5)
        assert(KnapSack(2,[3,2,1,1],[3,2,1,1]).branch_and_bound() == 2)
        assert(KnapSack(3,[2,2,2,2],[2,1,1,1]).branch_and_bound() == 2)
        assert(KnapSack(9,[2,2,2,2],[2,1,1,1]).branch_and_bound() == 5)
        assert(KnapSack(9,[5,5,4],[10,10,4]).branch_and_bound() == 14)
        assert(KnapSack(9,[7,5,4],[14,9,7]).branch_and_bound() == 16)
        
    def test_dynamic_prog(self):
        assert(KnapSack(1,[2,2,2],[2,1,3]).dynamic_prog() == 0)
        assert(KnapSack(4,[1,1,1,2],[3,2,1,1]).dynamic_prog() == 6)
        assert(KnapSack(3,[1,1,1,2],[3,2,1,1]).dynamic_prog() == 6)
        assert(KnapSack(2,[1,1,1,2],[3,2,1,1]).dynamic_prog() == 5)
        assert(KnapSack(2,[3,2,1,1],[3,2,1,1]).dynamic_prog() == 2)
        assert(KnapSack(3,[2,2,2,2],[2,1,1,1]).dynamic_prog() == 2)
        assert(KnapSack(9,[2,2,2,2],[2,1,1,1]).dynamic_prog() == 5)
        assert(KnapSack(9,[5,5,4],[10,10,4]).dynamic_prog() == 14)
        assert(KnapSack(9,[7,5,4],[14,9,7]).dynamic_prog() == 16)
    def dynamic_prog_scale_change(self):
        assert(True)

if __name__ == '__main__':
    unittest.main()