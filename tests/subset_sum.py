import unittest
from .utils import describe_test, separator
from src.algorithm.knapsack.subset_sum import SubSet
import numpy as np

class TestSubSet_Sum(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Subset Sum")

    def run(self, test):
        result = super().run(test)
        print("\n" + "=" * 30 + "\n")
        return result

    def test_GramSchmidt(self):
        print()
        set = SubSet([17,6,12,14,24], 23)
        B_star = set.GramSchmidt([[10,10],[13,-3]])
        assert np.array_equal(B_star, [[10, 10], [8, -8]])

        B_star= set.GramSchmidt([[1,1],[2,1]])
        assert np.array_equal(B_star, np.array([[1., 1.], [0.5, -0.5]]))
    
    def test_LLL(self):
        print()
        set = SubSet([17,6,12,14,24], 23)
        basis = set.LLL([[1,1],[2,1]])
        assert np.array_equal(basis, [[0., -1.], [1., 0.]])

        basis = set.LLL([[10,10],[13,-3]])
        assert np.array_equal(basis, [[10., 10.], [13., -3.]])

    def test_solve_LLL(self):
        print()
        solved_count = 0
        unsolved_count = 0
        total_density = 0

        print()
        for i in range(100):
            subset_problem = SubSet.generate_random_low_density_subset_problem(5,0.2)
            #print(f"Problem {i+1} : {subset_problem.set} {subset_problem.target}")
            X = subset_problem.solve_LLL()
            density = subset_problem.density()
            
            if X is not None:
                solved_count += 1
                total_density += density
            else:
                unsolved_count += 1

        avg_density = total_density / solved_count if solved_count > 0 else 0
        
        print("Benchmark Table:")
        print(f"Number of problems solved: {solved_count}")
        print(f"Number of problems unsolved: {unsolved_count}")
        print(f"Average density: {avg_density}")


    
    def test_solve_dynamic_prog(self):
        assert(SubSet([17,6,12,14,24]).solve_dynamic_prog() == (23,[17,6]))
        assert(SubSet([23603, 6105, 5851, 19660, 8398, 8545, 14712, 8554, 374 ,13457, 17831, 18309, 25025, 24879, 3145, 22588, 25765, 6105, 19660], 25765).solve_dynamic_prog() == (25765,[6105,19660]))

if __name__ == '__main__':
    unittest.main()