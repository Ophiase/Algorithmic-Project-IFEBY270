import numpy as np
import pulp

'''
    Find the pair of strategy (x, y) that corresponds to a nash equilibrium for a gain matrix A, B.
'''
class NashEquilibrium:
    def __init__(self, A : np.array, B : np.array):
        self.A = A
        self.B = B

        if A.shape != B.shape :
            raise ValueError()

        self.m = A.shape[0]
        self.n = A.shape[1]

        self.max_regret_a = np.max(A) - np.min(A)
        self.max_regret_b = np.max(B) - np.min(B)

    @staticmethod
    def _init_xrs_variables(i, x, r, s, letter, r_bound):
        x.append(pulp.LpVariable(f"x{letter}_{i}", lowBound=0, upBound=1)) # [0, 1]
        r.append(pulp.LpVariable(f"r{letter}_{i}", lowBound=0, upBound=r_bound)) # >= 0
        s.append(pulp.LpVariable(f"s{letter}_{i}", cat=pulp.LpBinary)) # {0, 1}
    
    def _init_variables(self):
        self.xa, self.xb = [], [] # strategies
        self.ra, self.rb = [], [] # regrets
        self.sa, self.sb = [], [] # supports

        for i in range(self.m) :
            NashEquilibrium._init_xrs_variables(
                i, self.xa, self.ra, self.sa, "a", self.max_regret_a)
        for j in range(self.n):
            NashEquilibrium._init_xrs_variables(
                j, self.xb, self.rb, self.sb, "b", self.max_regret_b)
            
        gain_a = pulp.LpVariable("gain_a", lowBound=0)
        gain_b = pulp.LpVariable("gain_b", lowBound=0)

    def solve(self, verbose = True) -> np.array:
        self.prob = pulp.LpProblem("Nash Equilibrium", pulp.LpMinimize)

        # VARIABLES
        self._init_variables()

        raise NotImplementedError()

        # CONSTRAINTS

        # OBJECTIVE FUNCTION

        self.prob += pulp.lpSum(ra) + pulp.lpSum(rb)

        # SOLVE

        with contextlib.redirect_stdout(None):
            self.prob.solve()
    
        if verbose :
            print(f"Status: {pulp.LpStatus[self.prob.status]}")
            for v in self.prob.variables():
                print(f"{v.name}: {v.value()}")
            print(f"Objective: {pulp.value(self.prob.objective)}")
        
        self.solution = pulp.value(prob.objective)

        return solution
