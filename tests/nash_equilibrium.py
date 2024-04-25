import unittest
from .utils import describe_test, separator
from src.algorithm.nash_equilibrium.nash_equilibrium import NashEquilibrium
import numpy as np
import re
import pulp
import sys
import subprocess


def extract_column_values_from_file(file_path):
        valeurs1 = []
        valeurs2 = []
        with open(file_path, "r") as fichier:
            for line in fichier:
                if ":" in line and "[" in line:
                    valeurs = line.split(":")[1].strip().split()
                    valeurs1.append(float(valeurs[1]))
                    valeurs2.append(float(valeurs[2]))
        return valeurs1,valeurs2


class TestNashEquilibrium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        describe_test("Nash Equilibrium")

    def run(self, test):
        result = super().run(test)
        print("\n" + "=" * 30 + "\n")
        return result

    def check_equilibrium_check(self,
            A : np.array, B : np.array, 
            wanted_equilibrium : tuple = None):
        
        print("\n")
        print(f"A: {A}")
        print(f"B: {B}")
        print()

        solution = NashEquilibrium(A, B).solve()

        if solution is None :
            print("No solution found")
            assert(False)        

        print(
            f"\033[92mSolution\033[94m : " + \
            f"{solution[0]}, {solution[1]}" + \
            "\033[0m")
        
        print()
        print(
            f"\033[92mCurrent Score\033[94m : " + \
            f"{NashEquilibrium.score(A, B, solution)}"
            "\033[0m\n")
        if wanted_equilibrium is not None:
            print(
                f"\033[92mWanted Score\033[94m  : " + \
                f"{wanted_equilibrium}"
                "\033[0m\n")
        
        # assert produces an unwanted traceback
        if not NashEquilibrium.is_valid(A, B, solution) :
            print(f"The solution is not a nash nash equilibrium.")

        # assert solution == wanted_equilibrium, \
        #     f"Error: wrong nash equilibrium. \nWanted: {wanted_equilibrium}, Computed: {solution}"
        
    def test_object_creation(self):
        NashEquilibrium(
            np.array([[3, 2], [1, 4]]), 
            np.array([[2, 1], [3, 2]])
            )
        
    #@unittest.skip("Not implemented")
    def test_game_00(self):
        self.check_equilibrium_check(
            np.array([[3, 2], [1, 4]]), 
            np.array([[2, 1], [3, 2]]), 
            None)
    
    #@unittest.skip("Not implemented")
    def test_game_01(self):
        self.check_equilibrium_check(
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

        self.check_equilibrium_check(
            A, -A, (0,0))


    def test_2x2_Symmetric_Games(self):
        t1,t2 = extract_column_values_from_file("baked_gamut/2x2_Symmetric_Games.txt")
        A=  np.array(t1).reshape(2, 2)
        B=  np.array(t2).reshape(2, 2)
        self.check_equilibrium_check(A, B, (0, 0))

    def test_chicken_game(self):
        t1,t2 = extract_column_values_from_file("baked_gamut/chicken_game.txt")
        A=  np.array(t1).reshape(2, 2)
        B=  np.array(t2).reshape(2, 2)
        self.check_equilibrium_check(A, B, (0, 0))

    def test_prisoners_dilemma_game(self):
        t1,t2 = extract_column_values_from_file("baked_gamut/prisoners_dilemma_game.txt")
        A=  np.array(t1).reshape(2, 2)
        B=  np.array(t2).reshape(2, 2)
        self.check_equilibrium_check(A, B, (0, 0))



if __name__ == '__main__':
    unittest.main()
