import unittest
from .utils import describe_test
from src.algorithm.nash_equilibrium.nash_equilibrium import NashEquilibrium
import numpy as np
import pulp

class TestNashEquilibrium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Nash Equilibrium")

    @staticmethod
    def check_equilibrium_check(
            A : np.array, B : np.array, 
            wanted_equilibrium : np.array):
        
        solution = NashEquilibrium(A, B).solve()
        assert solution == wanted_equilibrium, \
            f"Error: wrong nash equilibrium. \nWanted: {wanted_equilibrium}, Computed: {solution}"
        
    def test_object_creation(self):
        NashEquilibrium(
            np.array([[3, 2], [1, 4]]), 
            np.array([[2, 1], [3, 2]])
            )
        
    @unittest.skip("Not implemented")
    def test_game_00(self):
        TestNashEquilibrium.check_equilibrium_check(
            np.array([[3, 2], [1, 4]]), 
            np.array([[2, 1], [3, 2]]), 
            3)
    
    @unittest.skip("Not implemented")
    def test_game_01(self):
        TestNashEquilibrium.check_equilibrium_check(
            np.array([[1, 2], [3, 4]]), 
            np.array([[4, 3], [2, 1]]), 
            2)
        
if __name__ == '__main__':
    unittest.main()
