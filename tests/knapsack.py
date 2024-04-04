import unittest
from .utils import describe_test
from src.algorithm.knapsack.knapsack import KnapSack

class TestKnapSack(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Knap Sack")

    def test_upper_bound(self):
        assert(KnapSack(4,[1,1,1,2],[3,2,1,1]).upper_bound() == 6.5)
        assert(KnapSack(3,[1,1,1,2],[3,2,1,1]).upper_bound() == 6.0)
        assert(KnapSack(2,[1,1,1,2],[3,2,1,1]).upper_bound() == 5.0)
        assert(KnapSack(2,[3,2,1,1],[3,2,1,1]).upper_bound() == 2.0)
        assert(KnapSack(3,[2,2,2,2],[2,1,1,1]).upper_bound() == 2.5)
        assert(KnapSack(9,[2,2,2,2],[2,1,1,1]).upper_bound() == 5.0)
        assert(KnapSack(9,[5,5,4],[10,10,4]).upper_bound() == 18.0)
        
    def test_lower_bound(self):
        assert(KnapSack(4,[1,1,1,2],[3,2,1,1]).lower_bound() == 6)
        assert(KnapSack(3,[1,1,1,2],[3,2,1,1]).lower_bound() == 6)
        assert(KnapSack(2,[1,1,1,2],[3,2,1,1]).lower_bound() == 5)
        assert(KnapSack(2,[3,2,1,1],[3,2,1,1]).lower_bound() == 2)
        assert(KnapSack(3,[2,2,2,2],[2,1,1,1]).lower_bound() == 2)
        assert(KnapSack(9,[2,2,2,2],[2,1,1,1]).lower_bound() == 5)
        assert(KnapSack(9,[5,5,4],[10,10,4]).lower_bound() == 14)
    

if __name__ == '__main__':
    unittest.main()