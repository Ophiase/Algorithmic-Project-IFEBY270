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
            wanted_equilibrium : tuple):
        
        print(f"A: {A}")
        print(f"B: {B}")
        print()

        solution = NashEquilibrium(A, B).solve()

        print(
            f"\033[92mSolution\033[94m : " + \
            f"{solution[0]}, {solution[1]}" + \
            "\033[0m")
        
        print(
            f"\033[92mScore\033[94m : " + \
            f"{NashEquilibrium.score(A, B, solution)}"
            "\033[0m\n")

        # assert solution == wanted_equilibrium, \
        #     f"Error: wrong nash equilibrium. \nWanted: {wanted_equilibrium}, Computed: {solution}"
        
    def test_object_creation(self):
        NashEquilibrium(
            np.array([[3, 2], [1, 4]]), 
            np.array([[2, 1], [3, 2]])
            )
        
    #@unittest.skip("Not implemented")
    def test_game_00(self):
        TestNashEquilibrium.check_equilibrium_check(
            np.array([[3, 2], [1, 4]]), 
            np.array([[2, 1], [3, 2]]), 
            None)
    
    #@unittest.skip("Not implemented")
    def test_game_01(self):
        TestNashEquilibrium.check_equilibrium_check(
            np.array([[1, 2], [3, 4]]), 
            np.array([[4, 3], [2, 1]]), 
            None)
        
    #@unittest.skip("Not implemented")
    def test_game_paper_rock_scissor(self):
        A = np.array([
            [1,0,-1],
            [0,-1,1],
            [-1,1,0]
        ])

        TestNashEquilibrium.check_equilibrium_check(
            A, -A, (0,0))
        
if __name__ == '__main__':
    unittest.main()
